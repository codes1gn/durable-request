import { HashRouter, Routes, Route } from "react-router-dom";
import { Navbar } from "./components/Navbar";
import { Footer } from "./components/Footer";
import { Home } from "./pages/Home";
import { Changelog } from "./pages/Changelog";
import { CLISession } from "./pages/CLISession";
import { Roadmap } from "./pages/Roadmap";
import { Steering } from "./pages/Steering";

export function App() {
  return (
    <HashRouter>
      <div className="min-h-screen">
        <Navbar />
        <main className="pt-16">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/changelog" element={<Changelog />} />
            <Route path="/roadmap" element={<Roadmap />} />
            <Route path="/cli-session" element={<CLISession />} />
            <Route path="/steering" element={<Steering />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </HashRouter>
  );
}
