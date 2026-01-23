import { Bot, CheckCircle2 } from "lucide-react";
import { useEffect, useState } from "react";
import Dashboard from "./components/Dashboard";
import LeadCard from "./components/LeadCard";
import LeadForm from "./components/LeadForm";
import { healthCheck } from "./services/api";

function App() {
  const [leads, setLeads] = useState([]);
  const [apiStatus, setApiStatus] = useState("checking");
  const [showSuccess, setShowSuccess] = useState(false);

  useEffect(() => {
    checkAPIHealth();
  }, []);

  const checkAPIHealth = async () => {
    try {
      await healthCheck();
      setApiStatus("connected");
    } catch (error) {
      setApiStatus("error");
      console.error("API health check failed:", error);
    }
  };

  const handleLeadQualified = (result) => {
    if (result.success && result.qualified_lead) {
      setLeads([result.qualified_lead, ...leads]);
      setShowSuccess(true);
      setTimeout(() => setShowSuccess(false), 3000);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="bg-blue-600 p-2 rounded-lg">
                <Bot className="w-8 h-8 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">
                  AI Lead Agent
                </h1>
                <p className="text-sm text-gray-600">
                  Intelligent Lead Qualification System
                </p>
              </div>
            </div>

            <div className="flex items-center gap-2">
              <div
                className={`w-2 h-2 rounded-full ${
                  apiStatus === "connected"
                    ? "bg-green-500"
                    : apiStatus === "checking"
                      ? "bg-yellow-500"
                      : "bg-red-500"
                }`}
              />
              <span className="text-sm text-gray-600">
                {apiStatus === "connected"
                  ? "API Connected"
                  : apiStatus === "checking"
                    ? "Checking..."
                    : "API Error"}
              </span>
            </div>
          </div>
        </div>
      </header>

      {/* Success Toast */}
      {showSuccess && (
        <div className="fixed top-4 right-4 z-50 bg-green-500 text-white px-6 py-3 rounded-lg shadow-lg flex items-center gap-2 animate-bounce">
          <CheckCircle2 size={20} />
          <span className="font-medium">Lead qualified successfully!</span>
        </div>
      )}

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Dashboard Stats */}
        {leads.length > 0 && <Dashboard leads={leads} />}

        {/* Lead Form */}
        <div className="mb-8">
          <LeadForm onLeadQualified={handleLeadQualified} />
        </div>

        {/* Leads List */}
        {leads.length > 0 ? (
          <div>
            <h2 className="text-2xl font-bold text-gray-900 mb-6">
              Qualified Leads ({leads.length})
            </h2>
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {leads.map((lead, idx) => (
                <LeadCard key={idx} lead={lead} />
              ))}
            </div>
          </div>
        ) : (
          <div className="bg-white rounded-lg shadow-lg p-12 text-center">
            <Bot className="w-16 h-16 text-gray-400 mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-gray-700 mb-2">
              No leads yet
            </h3>
            <p className="text-gray-500">
              Submit a lead above to see AI-powered qualification in action
            </p>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <p className="text-center text-sm text-gray-500">
            Powered by Google Gemini AI • FastAPI • React
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App;
