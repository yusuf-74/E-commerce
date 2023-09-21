import { BrowserRouter, Routes, Route } from 'react-router-dom';
import './global.css';
import Landing from './pages/Landing';
import Login from './pages/auth/Login';
import Register from './pages/auth/Register';
import NavBar from './components/bars/NavBar';
import { useEffect } from 'react';
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

function App() {

  useEffect(() => {
    const script = document.createElement('script');
    script.setAttribute('src', 'https://accounts.google.com/gsi/client');
    script.setAttribute('async', true);
    document.head.appendChild(script);
  }, [])

  return (
    <div>
      <BrowserRouter>
        <NavBar />
        <Routes>
          <Route path='/' element={<Landing />} />
          <Route path='auth/login' element={<Login />} />
          <Route path='auth/register' element={<Register />} />
        </Routes>

      </BrowserRouter>
      <ToastContainer
        position="bottom-left"
        autoClose={7000}
        hideProgressBar={false}
        newestOnTop={false}
        closeOnClick
        rtl={false}
        pauseOnFocusLoss
        draggable
        pauseOnHover
        theme="light"
        style={{
          width: "auto",
        }}
      />
    </div>

  );
}

export default App;
