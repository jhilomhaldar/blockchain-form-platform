import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { getSubmissionDashboard } from "../services/api.js";

function SubmissionsDashboard() {
  const [submissions, setSubmissions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const shortValue = (value, start = 10, end = 8) => {
    if (!value) return "—";
    if (value.length <= start + end) return value;
    return `${value.slice(0, start)}...${value.slice(-end)}`;
  };

  const formatDate = (value) => {
    if (!value) return "—";
    return new Date(value).toLocaleString();
  };

  useEffect(() => {
    const loadSubmissions = async () => {
      try {
        setLoading(true);
        const data = await getSubmissionDashboard();
        setSubmissions(data.results || []);
      } catch (err) {
        setError(
          err.response?.data?.detail ||
            "Unable to load submissions dashboard. Please check backend server."
        );
      } finally {
        setLoading(false);
      }
    };

    loadSubmissions();
  }, []);

  return (
    <section className="card dashboard-card">
      <div className="section-heading">
        <div>
          <h2>Submissions Dashboard</h2>
          <p>
            Latest form submissions stored in PostgreSQL with blockchain proof
            transaction details.
          </p>
        </div>

        <Link className="secondary-link" to="/forms/contact-verification-form">
          + New Submission
        </Link>
      </div>

      {loading && <p>Loading submissions...</p>}

      {error && <div className="alert alert-error">{error}</div>}

      {!loading && !error && submissions.length === 0 && (
        <div className="empty-state">
          <h3>No submissions yet</h3>
          <p>Submit the demo form first to see records here.</p>
        </div>
      )}

      {!loading && !error && submissions.length > 0 && (
        <div className="table-wrap">
          <table className="dashboard-table">
            <thead>
              <tr>
                <th>Submission Ref</th>
                <th>Form</th>
                <th>Name</th>
                <th>Email</th>
                <th>Wallet</th>
                <th>Blockchain</th>
                <th>Verification</th>
                <th>Tx Hash</th>
                <th>Created</th>
                <th>Action</th>
              </tr>
            </thead>

            <tbody>
              {submissions.map((item) => (
                <tr key={item.id}>
                  <td>
                    <strong>{item.submission_ref}</strong>
                  </td>
                  <td>{item.form_title}</td>
                  <td>{item.name || "—"}</td>
                  <td>{item.email || "—"}</td>
                  <td title={item.wallet_address}>
                    {shortValue(item.wallet_address)}
                  </td>
                  <td>
                    <span className="status-pill">
                      {item.blockchain_status || "—"}
                    </span>
                  </td>
                  <td>
                    <span className="status-pill">
                      {item.verification_status || "—"}
                    </span>
                  </td>
                  <td title={item.blockchain_tx_hash}>
                    {shortValue(item.blockchain_tx_hash)}
                  </td>
                  <td>{formatDate(item.created_at)}</td>
                  <td>
                    <div className="table-actions">
                        <Link
                        className="table-action"
                        to={`/verify/${item.submission_ref}`}
                        >
                        Verify
                        </Link>

                        <Link
                        className="table-action table-action-light"
                        to={`/certificate/${item.submission_ref}`}
                        >
                        Certificate
                        </Link>
                    </div>
                </td>
            </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </section>
  );
}

export default SubmissionsDashboard;