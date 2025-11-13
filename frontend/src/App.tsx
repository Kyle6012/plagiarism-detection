import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import UploadForm from './components/UploadForm';
import LoginPage from './components/LoginPage';
import RegisterPage from './components/RegisterPage';
import DashboardPage from './components/DashboardPage';
import LandingPage from './components/LandingPage';

function App() {
  // In a real app, this would be based on authentication state
  const isLoggedIn = false;

  return (
    <Router>
      <div className="min-h-screen bg-dark-gray text-white">
        <div className="relative isolate min-h-screen bg-dark-gray text-white">
          <div className="absolute inset-x-0 top-[-10rem] -z-10 transform-gpu overflow-hidden blur-3xl sm:top-[-20rem]">
            <svg className="relative left-[calc(50%-11rem)] -z-10 h-[21.1875rem] max-w-none -translate-x-1/2 rotate-[30deg] sm:left-[calc(50%-30rem)] sm:h-[42.375rem]" viewBox="0 0 1155 678">
              <path fill="url(#45de2b6b-92d5-4d6d-a64a-26bdfb774304)" fillOpacity=".3" d="M317.219 518.975L203.852 678 0 438.341l317.219 80.634 204.172-286.402c1.307 132.337 45.083 346.658 209.733 145.248C936.936 126.058 882.053-94.234 1031.02 41.331c119.18 108.451 130.68 295.337 121.53 375.223L855 299l21.173 362.054-558.954-142.079z" />
              <defs>
                <linearGradient id="45de2b6b-92d5-4d6d-a64a-26bdfb774l04" x1="1155.49" x2="-78.208" y1=".177" y2="474.645" gradientUnits="userSpaceOnUse">
                  <stop stopColor="#9089FC" />
                  <stop offset="1" stopColor="#FF80B5" />
                </linearGradient>
              </defs>
            </svg>
          </div>
          <nav className="bg-dark-blue p-4">
            <div className="container mx-auto flex justify-between items-center">
              <Link to="/" className="text-xl font-bold">Plagiarism Detection</Link>
              <div>
                {isLoggedIn ? (
                  <>
                    <Link to="/upload" className="mr-4">Upload</Link>
                    <Link to="/dashboard" className="mr-4">Dashboard</Link>
                    {/* Add a logout button here */}
                  </>
                ) : (
                  <>
                    <Link to="/login" className="mr-4">Login</Link>
                    <Link to="/register">Register</Link>
                  </>
                )}
              </div>
            </div>
          </nav>
          <div className="container mx-auto p-4">
            <Routes>
              <Route path="/" element={<LandingPage />} />
              <Route path="/login" element={<LoginPage />} />
              <Route path="/register" element={<RegisterPage />} />
              <Route path="/upload" element={<UploadForm />} />
              <Route path="/dashboard" element={<DashboardPage />} />
            </Routes>
          </div>
        </div>
      </div>
    </Router>
  );
}

export default App;
