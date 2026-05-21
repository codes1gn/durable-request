import { useEffect } from "react";
import { HashRouter, Routes, Route, useLocation } from "react-router-dom";
import { Navbar } from "./components/Navbar";
import { Footer } from "./components/Footer";
import { Home } from "./pages/Home";
import { Changelog } from "./pages/Changelog";
import { CLISession } from "./pages/CLISession";
import { Roadmap } from "./pages/Roadmap";
import { Steering } from "./pages/Steering";
import { EnhanceMe } from "./pages/EnhanceMe";
import { DeepSleep } from "./pages/DeepSleep";
import { HealthCheck } from "./pages/HealthCheck";

function ScrollToTop() {
  const { pathname } = useLocation();
  useEffect(() => { window.scrollTo(0, 0); }, [pathname]);
  return null;
}

export function App() {
  return (
    <HashRouter>
      <ScrollToTop />
      <div className="min-h-screen">
        <Navbar />
        <main className="pt-16">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/changelog" element={<Changelog />} />
            <Route path="/roadmap" element={<Roadmap />} />
            <Route path="/cli-session" element={<CLISession />} />
            <Route path="/steering" element={<Steering />} />
            <Route path="/enhance-me" element={<EnhanceMe />} />
            <Route path="/deep-sleep" element={<DeepSleep />} />
            <Route path="/health" element={<HealthCheck />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </HashRouter>
  );
}
