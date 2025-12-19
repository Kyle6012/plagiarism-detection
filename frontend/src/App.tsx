import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './components/AuthProvider';
import MainLayout from './components/MainLayout';
import LandingPage from './components/LandingPage';
import LoginPage from './components/LoginPage';
import RegisterPage from './components/RegisterPage';
import DashboardPage from './components/DashboardPage';
import UploadForm from './components/UploadForm';
import AIDetectionPage from './components/AIDetectionPage';
import AdminPage from './components/AdminPage';
import './index.css';

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/" element={<MainLayout />}>
            <Route index element={<LandingPage />} />
            <Route path="login" element={<LoginPage />} />
            <Route path="register" element={<RegisterPage />} />
            <Route path="dashboard" element={<DashboardPage />} />
            <Route path="upload" element={<UploadForm />} />
            <Route path="ai-check" element={<AIDetectionPage />} />
            <Route path="admin" element={<AdminPage />} />
          </Route>
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;
