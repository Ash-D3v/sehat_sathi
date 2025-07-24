import './App.css';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import LandingPage from '../src/pages/LandingPage.jsx';
import Dashboard from './pages/DashBoard.jsx';
function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/landing" element={<LandingPage />} />
        <Route path="/dashboard" element={<Dashboard/>}/>
      </Routes>
    </BrowserRouter>
  );
}

export default App;