import { useState } from "react";
import { useParams } from "react-router-dom";
import { verifySubmission } from "../services/api";

function VerifySubmission() {
  const params = useParams();

  const [submissionRef, setSubmissionRef] = useState(params.submissionRef || "");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const handleVerify = async (e) => {
    e.preventDefault();

    if (!submissionRef.trim()) {
      setError("Please enter submission reference.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await verifySubmission(submissionRef.trim());
      setResult(response);
    } catch (err) {
      setError("Verification failed. Please check the submission reference.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page-grid single">
      <section className="card">
        <div className="section-header">
          <span className="badge">Verification</span>
          <h2>Verify Submission Proof</h2>
          <p>
            Compare the stored database hash with the blockchain proof stored in the smart contract.
          </p>
        </div>

        <form onSubmit={handleVerify} className="form-stack">
          <div className="form-group">
            <label>Submission Reference</label>
            <input
              value={submissionRef}
              onChange={(e) => setSubmissionRef(e.target.value)}
              placeholder="SUB-20260624-000001"
            />
          </div>

          {error && <div className="error-box">{error}</div>}

          <button type="submit" disabled={loading}>
            {loading ? "Verifying..." : "Verify Submission"}
          </button>
        </form>
      </section>

      {result && (
        <section className="card result-card">
          <h3>{result.verified ? "Verified Successfully" : "Verification Failed"}</h3>

          <div className="result-list">
            <div>
              <strong>Submission Ref</strong>
              <span>{result.submission_ref}</span>
            </div>

            <div>
              <strong>Stored DB Hash</strong>
              <span>{result.database?.stored_hash}</span>
            </div>

            <div>
              <strong>Regenerated DB Hash</strong>
              <span>{result.database?.regenerated_hash}</span>
            </div>

            <div>
              <strong>Blockchain Hash</strong>
              <span>{result.blockchain?.blockchain_hash || "Not available"}</span>
            </div>

            <div>
              <strong>Database Verified</strong>
              <span>{String(result.database?.verified)}</span>
            </div>

            <div>
              <strong>Blockchain Verified</strong>
              <span>{String(result.blockchain?.verified)}</span>
            </div>

            <div>
              <strong>Final Verification</strong>
              <span>{String(result.verified)}</span>
            </div>
          </div>
        </section>
      )}
    </div>
  );
}

export default VerifySubmission;