function Layout({ children }) {
  return (
    <div className="bg-blue-600 bg-center h-screen flex items-center justify-center">
      <div className="h-full bg-white absolute top-0 left-0 right-0 bottom-0 z-10 opacity-30"></div>
      {children}
    </div>
  );
}

export default Layout;
