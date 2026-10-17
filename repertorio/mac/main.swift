// Repertório para Mac: janela própria para o acervo e guarda que mantém o serviço ligado.
// Compile com ./repertorio/mac/build.sh (gera ~/Applications/Repertório.app).
import Cocoa
import WebKit

let endereco = URL(string: "http://127.0.0.1:8766/")!
let saude = URL(string: "http://127.0.0.1:8766/api/health")!
let acervo = URL(fileURLWithPath: #filePath).deletingLastPathComponent().deletingLastPathComponent().deletingLastPathComponent().path

let pagina = { (texto: String) in """
<html><body style="margin:0;height:100vh;display:grid;place-items:center;background:#121212;color:#ECE8E1;font:15px -apple-system,sans-serif">
<p>\(texto)</p></body></html>
""" }

final class App: NSObject, NSApplicationDelegate, WKNavigationDelegate, WKUIDelegate, WKDownloadDelegate {
    var janela: NSWindow?
    var web: WKWebView?
    var ultimaPartida = Date.distantPast
    var destinos: [ObjectIdentifier: URL] = [:]

    func applicationDidFinishLaunching(_ aviso: Notification) {
        montarMenu()
        garantir()
        Timer.scheduledTimer(withTimeInterval: 30, repeats: true) { [weak self] _ in self?.garantir() }
        // aberto pelo login: só mantém o serviço, sem janela
        if !CommandLine.arguments.contains("--login") { mostrar() }
    }

    func applicationShouldTerminateAfterLastWindowClosed(_ app: NSApplication) -> Bool { false }

    func applicationShouldHandleReopen(_ app: NSApplication, hasVisibleWindows: Bool) -> Bool {
        mostrar()
        return true
    }

    // MARK: serviço

    func verificar(_ fim: @escaping (Bool) -> Void) {
        var pedido = URLRequest(url: saude, cachePolicy: .reloadIgnoringLocalCacheData, timeoutInterval: 2)
        pedido.httpMethod = "GET"
        URLSession.shared.dataTask(with: pedido) { _, resposta, _ in
            let ok = (resposta as? HTTPURLResponse)?.statusCode == 200
            DispatchQueue.main.async { fim(ok) }
        }.resume()
    }

    /// Confere o serviço e, se não responder, liga de novo (no máximo uma tentativa a cada 20 s).
    func garantir(_ depois: ((Bool) -> Void)? = nil) {
        verificar { ok in
            if !ok && Date().timeIntervalSince(self.ultimaPartida) > 20 {
                self.ultimaPartida = Date()
                let processo = Process()
                processo.executableURL = URL(fileURLWithPath: "/bin/sh")
                processo.currentDirectoryURL = URL(fileURLWithPath: acervo)
                processo.arguments = ["-c", "/usr/bin/nohup /bin/sh repertorio/run.sh serve >> \"$HOME/Library/Logs/repertorio.log\" 2>&1 &"]
                try? processo.run()
            }
            depois?(ok)
        }
    }

    // MARK: janela

    func mostrar() {
        if janela == nil { criarJanela() }
        janela?.makeKeyAndOrderFront(nil)
        NSApp.activate(ignoringOtherApps: true)
    }

    func criarJanela() {
        let configuracao = WKWebViewConfiguration()
        configuracao.websiteDataStore = .default()
        let visao = WKWebView(frame: .zero, configuration: configuracao)
        visao.navigationDelegate = self
        visao.uiDelegate = self
        visao.allowsMagnification = true
        let j = NSWindow(contentRect: NSRect(x: 0, y: 0, width: 1440, height: 900),
                         styleMask: [.titled, .closable, .miniaturizable, .resizable],
                         backing: .buffered, defer: false)
        j.title = "Repertório"
        j.contentView = visao
        j.minSize = NSSize(width: 720, height: 480)
        j.isReleasedWhenClosed = false
        j.backgroundColor = NSColor(red: 0.07, green: 0.07, blue: 0.07, alpha: 1)
        j.center()
        j.setFrameAutosaveName("Repertorio")
        janela = j
        web = visao
        carregar()
    }

    func carregar() {
        web?.loadHTMLString(pagina("Ligando o Repertório..."), baseURL: nil)
        aguardar(60)
    }

    func aguardar(_ tentativas: Int) {
        garantir { ok in
            if ok {
                self.web?.load(URLRequest(url: endereco))
            } else if tentativas > 0 {
                DispatchQueue.main.asyncAfter(deadline: .now() + 0.5) { self.aguardar(tentativas - 1) }
            } else {
                self.web?.loadHTMLString(pagina("Não consegui ligar o Repertório. Tente ⌘R em alguns segundos."), baseURL: nil)
            }
        }
    }

    // MARK: navegação: o acervo fica na janela; links de fora abrem no navegador

    func local(_ url: URL?) -> Bool {
        guard let url, let esquema = url.scheme, esquema.hasPrefix("http") else { return true }
        return url.host == "127.0.0.1" || url.host == "localhost"
    }

    func webView(_ visao: WKWebView, decidePolicyFor acao: WKNavigationAction,
                 decisionHandler: @escaping (WKNavigationActionPolicy) -> Void) {
        if acao.shouldPerformDownload { return decisionHandler(.download) }
        if !local(acao.request.url), let url = acao.request.url {
            NSWorkspace.shared.open(url)
            return decisionHandler(.cancel)
        }
        decisionHandler(.allow)
    }

    func webView(_ visao: WKWebView, decidePolicyFor resposta: WKNavigationResponse,
                 decisionHandler: @escaping (WKNavigationResponsePolicy) -> Void) {
        let anexo = (resposta.response as? HTTPURLResponse)?
            .value(forHTTPHeaderField: "Content-Disposition")?.lowercased().hasPrefix("attachment") ?? false
        decisionHandler(anexo || !resposta.canShowMIMEType ? .download : .allow)
    }

    func webView(_ visao: WKWebView, createWebViewWith configuracao: WKWebViewConfiguration,
                 for acao: WKNavigationAction, windowFeatures: WKWindowFeatures) -> WKWebView? {
        if let url = acao.request.url {
            if local(url) { visao.load(acao.request) } else { NSWorkspace.shared.open(url) }
        }
        return nil
    }

    func webView(_ visao: WKWebView, runJavaScriptAlertPanelWithMessage mensagem: String,
                 initiatedByFrame quadro: WKFrameInfo, completionHandler: @escaping () -> Void) {
        let alerta = NSAlert()
        alerta.messageText = mensagem
        alerta.runModal()
        completionHandler()
    }

    func webView(_ visao: WKWebView, runJavaScriptConfirmPanelWithMessage mensagem: String,
                 initiatedByFrame quadro: WKFrameInfo, completionHandler: @escaping (Bool) -> Void) {
        let alerta = NSAlert()
        alerta.messageText = mensagem
        alerta.addButton(withTitle: "OK")
        alerta.addButton(withTitle: "Cancelar")
        completionHandler(alerta.runModal() == .alertFirstButtonReturn)
    }

    // MARK: downloads: você escolhe onde salvar

    func webView(_ visao: WKWebView, navigationAction: WKNavigationAction, didBecome download: WKDownload) {
        download.delegate = self
    }

    func webView(_ visao: WKWebView, navigationResponse: WKNavigationResponse, didBecome download: WKDownload) {
        download.delegate = self
    }

    func download(_ download: WKDownload, decideDestinationUsing resposta: URLResponse,
                  suggestedFilename nome: String, completionHandler: @escaping (URL?) -> Void) {
        let painel = NSSavePanel()
        painel.nameFieldStringValue = nome
        painel.canCreateDirectories = true
        guard let janela else { return completionHandler(nil) }
        painel.beginSheetModal(for: janela) { escolha in
            guard escolha == .OK, let url = painel.url else { return completionHandler(nil) }
            try? FileManager.default.removeItem(at: url)
            self.destinos[ObjectIdentifier(download)] = url
            completionHandler(url)
        }
    }

    func downloadDidFinish(_ download: WKDownload) {
        if let url = destinos.removeValue(forKey: ObjectIdentifier(download)) {
            NSWorkspace.shared.activateFileViewerSelecting([url])
        }
    }

    func download(_ download: WKDownload, didFailWithError erro: Error, resumeData: Data?) {
        destinos.removeValue(forKey: ObjectIdentifier(download))
        if let janela { NSAlert(error: erro).beginSheetModal(for: janela) }
    }

    // MARK: menu

    @objc func recarregar() {
        if web?.url?.host == endereco.host { web?.reload() } else { carregar() }
    }
    @objc func zoomReal() { web?.pageZoom = 1 }
    @objc func zoomMais() { web?.pageZoom = min((web?.pageZoom ?? 1) + 0.1, 3) }
    @objc func zoomMenos() { web?.pageZoom = max((web?.pageZoom ?? 1) - 0.1, 0.5) }
    @objc func novaJanela() { mostrar() }

    func montarMenu() {
        let principal = NSMenu()
        func submenu(_ titulo: String, _ itens: [NSMenuItem]) -> NSMenu {
            let item = NSMenuItem()
            let menu = NSMenu(title: titulo)
            itens.forEach(menu.addItem)
            item.submenu = menu
            principal.addItem(item)
            return menu
        }
        func item(_ titulo: String, _ acao: Selector, _ tecla: String = "", _ alvo: AnyObject? = nil,
                  _ modificadores: NSEvent.ModifierFlags = .command) -> NSMenuItem {
            let i = NSMenuItem(title: titulo, action: acao, keyEquivalent: tecla)
            i.target = alvo
            i.keyEquivalentModifierMask = modificadores
            return i
        }
        _ = submenu("Repertório", [
            item("Sobre o Repertório", #selector(NSApplication.orderFrontStandardAboutPanel(_:))),
            .separator(),
            item("Ocultar Repertório", #selector(NSApplication.hide(_:)), "h"),
            item("Ocultar os outros", #selector(NSApplication.hideOtherApplications(_:)), "h", nil, [.command, .option]),
            .separator(),
            item("Encerrar Repertório", #selector(NSApplication.terminate(_:)), "q"),
        ])
        _ = submenu("Editar", [
            item("Desfazer", Selector(("undo:")), "z"),
            item("Refazer", Selector(("redo:")), "z", nil, [.command, .shift]),
            .separator(),
            item("Recortar", #selector(NSText.cut(_:)), "x"),
            item("Copiar", #selector(NSText.copy(_:)), "c"),
            item("Colar", #selector(NSText.paste(_:)), "v"),
            item("Selecionar tudo", #selector(NSText.selectAll(_:)), "a"),
        ])
        _ = submenu("Visualizar", [
            item("Recarregar", #selector(recarregar), "r", self),
            .separator(),
            item("Tamanho real", #selector(zoomReal), "0", self),
            item("Aumentar", #selector(zoomMais), "+", self),
            item("Diminuir", #selector(zoomMenos), "-", self),
            .separator(),
            item("Tela cheia", #selector(NSWindow.toggleFullScreen(_:)), "f", nil, [.command, .control]),
        ])
        let janelas = submenu("Janela", [
            item("Mostrar o Repertório", #selector(novaJanela), "n", self),
            item("Minimizar", #selector(NSWindow.performMiniaturize(_:)), "m"),
            item("Fechar", #selector(NSWindow.performClose(_:)), "w"),
        ])
        NSApp.mainMenu = principal
        NSApp.windowsMenu = janelas
    }
}

let aplicativo = NSApplication.shared
let delegado = App()
aplicativo.delegate = delegado
aplicativo.setActivationPolicy(.regular)
aplicativo.run()
