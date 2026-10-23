import React from 'react';
import {createRoot} from 'react-dom/client';
import {QueryClient,QueryClientProvider} from '@tanstack/react-query';
import App from './App';
import './style.css';
// Um erro inesperado numa tela não deixa o app em branco: oferece recarregar e limpar as preferências deste navegador.
class Guard extends React.Component<{children:React.ReactNode},{failed:boolean}>{
 state={failed:false};
 static getDerivedStateFromError(){return {failed:true};}
 componentDidCatch(error:unknown){console.error(error);}
 render(){
  if(!this.state.failed)return this.props.children;
  return <div className="empty crash-screen" role="alert"><h2>Algo deu errado nesta tela.</h2><p>Recarregue para continuar. Se o problema voltar, limpe as preferências deste navegador (tema, espaço aberto e câmera do mapa). Sua biblioteca não é afetada.</p><button onClick={()=>location.reload()}>Recarregar</button><button onClick={()=>{try{localStorage.clear();}catch{/* Sem acesso às preferências. */}location.reload();}}>Limpar preferências e recarregar</button></div>;
 }
}
const client=new QueryClient({defaultOptions:{queries:{retry:1,refetchOnWindowFocus:false}}});
createRoot(document.getElementById('root')!).render(<React.StrictMode><Guard><QueryClientProvider client={client}><App/></QueryClientProvider></Guard></React.StrictMode>);
