#!/bin/sh
# Gera o Repertório.app nativo (janela própria, R branco em fundo preto) no caminho indicado.
# Uso: ./app/mac/build.sh /caminho/Repertório.app
# O ícone aprovado vem de icone.png; conceito e procedência em ICONE.md.
set -eu
AQUI=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd -P)
RAIZ=$(CDPATH= cd -- "$AQUI/../.." && pwd -P)
APP=${1:?informe o caminho do .app}
OBRA=$(mktemp -d)
mkdir -p "$APP/Contents/MacOS" "$APP/Contents/Resources" "$OBRA/Repertorio.iconset"
ARQUITETURA=$(uname -m)
VERSAO=$(sed -n "s/^__version__ = '\(.*\)'$/\1/p" "$RAIZ/app/server/repertorio/__init__.py")
swiftc -O -target "$ARQUITETURA-apple-macos13" -o "$APP/Contents/MacOS/Repertorio" "$AQUI/main.swift" -framework Cocoa -framework WebKit
for s in 16 32 128 256 512; do
  sips -z $s $s "$AQUI/icone.png" --out "$OBRA/Repertorio.iconset/icon_${s}x${s}.png" >/dev/null
  sips -z $((s*2)) $((s*2)) "$AQUI/icone.png" --out "$OBRA/Repertorio.iconset/icon_${s}x${s}@2x.png" >/dev/null
done
iconutil -c icns -o "$APP/Contents/Resources/Repertorio.icns" "$OBRA/Repertorio.iconset"
cat > "$APP/Contents/Info.plist" <<'PLIST'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key><string>Repertorio</string>
    <key>CFBundleIdentifier</key><string>local.repertorio</string>
    <key>CFBundleName</key><string>Repertório</string>
    <key>CFBundleDisplayName</key><string>Repertório</string>
    <key>CFBundleIconFile</key><string>Repertorio</string>
    <key>CFBundlePackageType</key><string>APPL</string>
    <key>CFBundleShortVersionString</key><string>1.0</string>
    <key>CFBundleVersion</key><string>1</string>
    <key>LSMinimumSystemVersion</key><string>13.0</string>
    <key>LSApplicationCategoryType</key><string>public.app-category.productivity</string>
    <key>NSHighResolutionCapable</key><true/>
    <key>NSPrincipalClass</key><string>NSApplication</string>
    <key>NSAppTransportSecurity</key><dict><key>NSAllowsLocalNetworking</key><true/></dict>
</dict>
</plist>
PLIST
/usr/libexec/PlistBuddy -c "Set :CFBundleShortVersionString $VERSAO" "$APP/Contents/Info.plist"
/usr/libexec/PlistBuddy -c "Add :RepertorioProjectRoot string $RAIZ" "$APP/Contents/Info.plist"
codesign --force -s - "$APP"
echo "$APP"
