import './App.css';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import LandingPage from '../src/pages/LandingPage.jsx';
function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/landing" element={<LandingPage />} />

      </Routes>
    </BrowserRouter>
  );
}

export default App;