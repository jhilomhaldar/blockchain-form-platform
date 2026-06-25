import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { getFormBySlug, submitForm } from "../services/api";
import WalletConnectButton from "../components/WalletConnectButton.jsx";

function SubmitForm() {
  const { slug } = useParams();

  const [form, setForm] = useState(null);
  const [values, setValues] = useState({});
  const [walletAddress, setWalletAddress] = useState(
    "0x1234567890abcdef1234567890abcdef12345678"
  );
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    loadForm();
  }, [slug]);

  const loadForm = async () => {
    try {
      setLoading(true);
      const response = await getFormBySlug(slug);
      setForm(response.data);

      const initialValues = {};
      response.data.fields.forEach((field) => {
        initialValues[field.key] = "";
      });

      setValues(initialValues);
    } catch (err) {
      setError("Unable to load form. Please make sure Django backend is running and the form exists.");
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (key, value) => {
    setValues((prev) => ({
      ...prev,
      [key]: value,
    }));
  };

  const renderField = (field) => {
    const commonProps = {
      value: values[field.key] || "",
      placeholder: field.placeholder || "",
      required: field.is_required,
      onChange: (e) => handleChange(field.key, e.target.value),
    };

    if (field.field_type === "TEXTAREA") {
      return <textarea {...commonProps} rows="5" />;
    }

    if (field.field_type === "EMAIL") {
      return <input type="email" {...commonProps} />;
    }

    if (field.field_type === "NUMBER") {
      return <input type="number" {...commonProps} />;
    }

    if (field.field_type === "DATE") {
      return <input type="date" {...commonProps} />;
    }

    return <input type="text" {...commonProps} />;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    setSubmitting(true);
    setError("");
    setResult(null);

    try {
      const payload = {
        form_slug: slug,
        wallet_address: walletAddress,
        submitted_data: values,
      };

      const response = await submitForm(payload);
      setResult(response);
    } catch (err) {
      const apiError = err.response?.data?.errors || err.response?.data?.message;
      setError(apiError ? JSON.stringify(apiError) : "Submission failed.");
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return <div className="card">Loading form...</div>;
  }

  if (error && !form) {
    return <div className="card error-box">{error}</div>;
  }

  return (
    <div className="page-grid">
      <section className="card">
        <div className="section-header">
          <span className="badge">Blockchain Ready</span>
          <h2>{form?.title}</h2>
          <p>{form?.description}</p>
        </div>

        <form onSubmit={handleSubmit} className="form-stack">
          <div className="form-group">
            <label>Wallet Address</label>

            <WalletConnectButton onWalletChange={setWalletAddress} />

            <input
                value={walletAddress}
                onChange={(e) => setWalletAddress(e.target.value)}
                placeholder="0x..."
            />

            <small>
                You can connect a wallet or manually enter a demo wallet address for local testing.
            </small>
            </div>

          {form?.fields?.map((field) => (
            <div className="form-group" key={field.id}>
              <label>
                {field.label}
                {field.is_required && <span className="required">*</span>}
              </label>
              {renderField(field)}
              {field.help_text && <small>{field.help_text}</small>}
            </div>
          ))}

          {error && <div className="error-box">{error}</div>}

          <button type="submit" disabled={submitting}>
            {submitting ? "Submitting..." : "Submit & Store Blockchain Proof"}
          </button>
        </form>
      </section>

      <section className="card result-card">
        <h3>Submission Result</h3>

        {!result && (
          <p className="muted">
            After submission, the database hash, blockchain transaction hash,
            and verification link will appear here.
          </p>
        )}

        {result && (
          <div className="result-list">
            <div>
              <strong>Submission Ref</strong>
              <span>{result.data.submission_ref}</span>
            </div>

            <div>
              <strong>Data Hash</strong>
              <span>{result.data.data_hash}</span>
            </div>

            <div>
              <strong>Blockchain Status</strong>
              <span>{result.data.blockchain_status}</span>
            </div>

            <div>
              <strong>Transaction Hash</strong>
              <span>{result.data.blockchain_tx_hash || "Not available"}</span>
            </div>

            <div>
              <strong>Blockchain Message</strong>
              <span>{result.blockchain?.message}</span>
            </div>

            <a className="verify-link" href={`/verify/${result.data.submission_ref}`}>
              Verify this submission
            </a>
          </div>
        )}
      </section>
    </div>
  );
}

export default SubmitForm;