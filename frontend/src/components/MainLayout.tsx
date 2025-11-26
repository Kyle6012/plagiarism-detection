import { Outlet } from 'react-router-dom';
import Navbar from './Navbar';

const MainLayout = () => {
  return (
    <>
      <Navbar />
      <main className="container" style={{ paddingTop: '80px', minHeight: 'calc(100vh - 80px)' }}>
        <Outlet />
      </main>
    </>
  );
};

export default MainLayout;
