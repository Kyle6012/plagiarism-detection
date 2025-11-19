import React from 'react';
import { NavLink } from 'react-router-dom';

const MainLayout = ({ children }: { children: React.ReactNode }) => {
  return (
    <div className="flex h-screen">
      <aside className="w-64 bg-color-surface text-color-text-primary p-4 fixed h-full">
        <h1 className="text-2xl font-bold mb-8 text-color-primary">Plagiarism Detection</h1>
        <nav className="flex flex-col space-y-2">
          <NavLink
            to="/dashboard"
            className={({ isActive }) =>
              `px-4 py-2 rounded-md ${isActive ? 'bg-color-primary text-white' : 'hover:bg-color-primary-hover hover:text-white'}`
            }
          >
            Dashboard
          </NavLink>
          <NavLink
            to="/upload"
            className={({ isActive }) =>
              `px-4 py-2 rounded-md ${isActive ? 'bg-color-primary text-white' : 'hover:bg-color-primary-hover hover:text-white'}`
            }
          >
            Upload
          </NavLink>
        </nav>
      </aside>
      <main className="flex-1 p-8 overflow-y-auto ml-64">
        {children}
      </main>
    </div>
  );
};

export default MainLayout;
