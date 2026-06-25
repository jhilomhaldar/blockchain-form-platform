import { Routes, Route, Link, Navigate } from "react-router-dom";
import SubmitForm from "./pages/SubmitForm.jsx";
import VerifySubmission from "./pages/VerifySubmission.jsx";
import SubmissionsDashboard from "./pages/SubmissionsDashboard.jsx";

function App() {
  return (
    <div className="app-shell">
      <header className="topbar">
        <div>
          <h1>Blockchain Form Platform</h1>
          <p>
            Secure form submission with PostgreSQL, Django, Solidity, and local blockchain proof verification.
          </p>
        </div>

        <nav>
          <Link to="/forms/contact-verification-form">Submit Form</Link>
          <Link to="/verify">Verify</Link>
          <Link to="/dashboard">Dashboard</Link>
        </nav>
      </header>

      <main>
        <Routes>
          <Route path="/" element={<Navigate to="/forms/contact-verification-form" replace />} />
          <Route path="/forms/:slug" element={<SubmitForm />} />
          <Route path="/verify" element={<VerifySubmission />} />
          <Route path="/verify/:submissionRef" element={<VerifySubmission />} />
          <Route path="/dashboard" element={<SubmissionsDashboard />} />
        </Routes>
      </main>
    </div>
  );
}

export default App;
