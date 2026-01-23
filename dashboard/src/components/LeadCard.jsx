import {
  Building2,
  Clock,
  Flame,
  Snowflake,
  ThermometerSun,
  TrendingUp,
  Users,
} from "lucide-react";

export default function LeadCard({ lead }) {
  const getPriorityColor = (priority) => {
    switch (priority) {
      case "hot":
        return "bg-red-100 text-red-800 border-red-300";
      case "warm":
        return "bg-orange-100 text-orange-800 border-orange-300";
      case "cold":
        return "bg-blue-100 text-blue-800 border-blue-300";
      default:
        return "bg-gray-100 text-gray-800 border-gray-300";
    }
  };

  const getPriorityIcon = (priority) => {
    switch (priority) {
      case "hot":
        return <Flame className="w-5 h-5" />;
      case "warm":
        return <ThermometerSun className="w-5 h-5" />;
      case "cold":
        return <Snowflake className="w-5 h-5" />;
      default:
        return null;
    }
  };

  const getScoreColor = (score) => {
    if (score >= 80) return "text-red-600";
    if (score >= 60) return "text-orange-600";
    return "text-blue-600";
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-6 hover:shadow-xl transition-shadow duration-200">
      {/* Header */}
      <div className="flex justify-between items-start mb-4">
        <div>
          <h3 className="text-xl font-bold text-gray-900">{lead.name}</h3>
          <p className="text-sm text-gray-600">{lead.email}</p>
          {lead.company && (
            <p className="text-sm text-gray-500 flex items-center gap-1 mt-1">
              <Building2 size={14} />
              {lead.company}
            </p>
          )}
        </div>

        <div className="flex flex-col items-end gap-2">
          <div
            className={`px-3 py-1 rounded-full border-2 flex items-center gap-1 ${getPriorityColor(lead.priority)}`}
          >
            {getPriorityIcon(lead.priority)}
            <span className="font-semibold text-sm uppercase">
              {lead.priority}
            </span>
          </div>
          <div className={`text-3xl font-bold ${getScoreColor(lead.score)}`}>
            {Math.round(lead.score)}
          </div>
        </div>
      </div>

      {/* Analysis */}
      <div className="space-y-3 border-t pt-4">
        {lead.analysis.industry && (
          <div className="flex items-start gap-2">
            <Building2 size={18} className="text-gray-400 mt-1" />
            <div>
              <p className="text-xs text-gray-500 uppercase tracking-wide">
                Industry
              </p>
              <p className="text-sm font-medium text-gray-900">
                {lead.analysis.industry}
              </p>
            </div>
          </div>
        )}

        {lead.analysis.company_size && (
          <div className="flex items-start gap-2">
            <Users size={18} className="text-gray-400 mt-1" />
            <div>
              <p className="text-xs text-gray-500 uppercase tracking-wide">
                Company Size
              </p>
              <p className="text-sm font-medium text-gray-900">
                {lead.analysis.company_size}
              </p>
            </div>
          </div>
        )}

        <div className="flex items-start gap-2">
          <Clock size={18} className="text-gray-400 mt-1" />
          <div>
            <p className="text-xs text-gray-500 uppercase tracking-wide">
              Urgency Level
            </p>
            <p className="text-sm font-medium text-gray-900 capitalize">
              {lead.analysis.urgency_level}
            </p>
          </div>
        </div>

        <div className="flex items-start gap-2">
          <TrendingUp size={18} className="text-gray-400 mt-1" />
          <div>
            <p className="text-xs text-gray-500 uppercase tracking-wide">
              Buying Intent
            </p>
            <p className="text-sm font-medium text-gray-900 capitalize">
              {lead.analysis.buying_intent.replace(/_/g, " ")}
            </p>
          </div>
        </div>

        {lead.analysis.pain_points && lead.analysis.pain_points.length > 0 && (
          <div className="mt-4">
            <p className="text-xs text-gray-500 uppercase tracking-wide mb-2">
              Pain Points
            </p>
            <div className="flex flex-wrap gap-2">
              {lead.analysis.pain_points.map((point, idx) => (
                <span
                  key={idx}
                  className="px-2 py-1 bg-purple-50 text-purple-700 text-xs rounded-full"
                >
                  {point}
                </span>
              ))}
            </div>
          </div>
        )}

        {lead.analysis.budget_signals &&
          lead.analysis.budget_signals.length > 0 && (
            <div className="mt-4">
              <p className="text-xs text-gray-500 uppercase tracking-wide mb-2">
                Budget Signals
              </p>
              <div className="flex flex-wrap gap-2">
                {lead.analysis.budget_signals.map((signal, idx) => (
                  <span
                    key={idx}
                    className="px-2 py-1 bg-green-50 text-green-700 text-xs rounded-full"
                  >
                    {signal}
                  </span>
                ))}
              </div>
            </div>
          )}

        {/* Recommended Action */}
        <div className="mt-4 p-4 bg-blue-50 rounded-lg border border-blue-200">
          <p className="text-xs text-blue-600 uppercase tracking-wide mb-1">
            Recommended Action
          </p>
          <p className="text-sm text-blue-900 font-medium">
            {lead.analysis.recommended_action}
          </p>
        </div>
      </div>

      {/* Message Preview */}
      <div className="mt-4 pt-4 border-t">
        <p className="text-xs text-gray-500 uppercase tracking-wide mb-2">
          Message
        </p>
        <p className="text-sm text-gray-700 line-clamp-3">{lead.message}</p>
      </div>
    </div>
  );
}
