import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { getSubmissionCertificate } from "../services/api.js";

function VerificationCertificate() {
  const { submissionRef } = useParams();

  const [certificate, setCertificate] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [copied, setCopied] = useState(false);

  const shortValue = (value, start = 14, end = 10) => {
    if (!value) return "—";
    if (value.length <= start + end) return value;
    return `${value.slice(0, start)}...${value.slice(-end)}`;
  };

  const formatDate = (value) => {
    if (!value) return "—";
    return new Date(value).toLocaleString();
  };

  const handlePrint = () => {
  window.print();
};

const handleCopyCertificateLink = async () => {
  try {
    await navigator.clipboard.writeText(window.location.href);
    setCopied(true);

    setTimeout(() => {
      setCopied(false);
    }, 2000);
  } catch (err) {
    setCopied(false);
  }
};

  useEffect(() => {
    const loadCertificate = async () => {
      try {
        setLoading(true);
        const data = await getSubmissionCertificate(submissionRef);
        setCertificate(data.certificate);
      } catch (err) {
        setError(
          err.response?.data?.message ||
            "Unable to load verification certificate."
        );
      } finally {
        setLoading(false);
      }
    };

    if (submissionRef) {
      loadCertificate();
    }
  }, [submissionRef]);

  return (
    <section className="certificate-page">
      {loading && <p>Generating verification certificate...</p>}

      {error && <div className="alert alert-error">{error}</div>}

      {!loading && !error && certificate && (
        <div className="certificate-card">
          <div className="certificate-header">
            <div>
              <span className="certificate-label">Blockchain Verification Certificate</span>
              <h2>
                {certificate.final_verified
                  ? "Submission Verified"
                  : "Verification Failed"}
              </h2>
              <p>
                This certificate confirms whether the submitted data hash matches
                the blockchain proof registered for this submission.
              </p>
            </div>

            <div
              className={
                certificate.final_verified
                  ? "certificate-seal certificate-seal-success"
                  : "certificate-seal certificate-seal-failed"
              }
            >
              {certificate.final_verified ? "VALID" : "FAILED"}
            </div>
          </div>

          <div className="certificate-grid">
            <div>
              <label>Submission Reference</label>
              <strong>{certificate.submission_ref}</strong>
            </div>

            <div>
              <label>Form</label>
              <strong>{certificate.form_title || "—"}</strong>
            </div>

            <div>
              <label>Submitted Name</label>
              <strong>{certificate.submitted_name || "—"}</strong>
            </div>

            <div>
              <label>Submitted Email</label>
              <strong>{certificate.submitted_email || "—"}</strong>
            </div>

            <div>
              <label>Wallet Address</label>
              <strong title={certificate.wallet_address}>
                {shortValue(certificate.wallet_address)}
              </strong>
            </div>

            <div>
              <label>Blockchain Status</label>
              <strong>{certificate.blockchain_status || "—"}</strong>
            </div>

            <div>
              <label>Database Hash Matched</label>
              <strong>{certificate.database_hash_matched ? "Yes" : "No"}</strong>
            </div>

            <div>
              <label>Blockchain Verified</label>
              <strong>{certificate.blockchain_verified ? "Yes" : "No"}</strong>
            </div>

            <div className="certificate-full">
              <label>Stored Data Hash</label>
              <code>{certificate.stored_data_hash || "—"}</code>
            </div>

            <div className="certificate-full">
              <label>Regenerated Data Hash</label>
              <code>{certificate.regenerated_data_hash || "—"}</code>
            </div>

            <div className="certificate-full">
              <label>Blockchain Transaction Hash</label>
              <code>{certificate.blockchain_tx_hash || "—"}</code>
            </div>

            <div>
              <label>Submitted At</label>
              <strong>{formatDate(certificate.submitted_at)}</strong>
            </div>

            <div>
              <label>Verified At</label>
              <strong>{formatDate(certificate.verified_at)}</strong>
            </div>
          </div>

          <div className="certificate-actions no-print">
            <Link to="/dashboard" className="secondary-link">
                Back to Dashboard
            </Link>

            <Link
                to={`/verify/${certificate.submission_ref}`}
                className="secondary-link"
            >
                Technical Verification
            </Link>

            <button type="button" className="secondary-link" onClick={handlePrint}>
                Print / Save PDF
            </button>

            <button
                type="button"
                className="secondary-link table-action-light"
                onClick={handleCopyCertificateLink}
            >
                {copied ? "Link Copied" : "Copy Certificate Link"}
            </button>
            </div>
        </div>
      )}
    </section>
  );
}

export default VerificationCertificate;