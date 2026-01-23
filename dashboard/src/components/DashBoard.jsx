import { Flame, Snowflake, ThermometerSun, TrendingUp } from "lucide-react";

export default function Dashboard({ leads }) {
  const stats = {
    total: leads.length,
    hot: leads.filter((l) => l.priority === "hot").length,
    warm: leads.filter((l) => l.priority === "warm").length,
    cold: leads.filter((l) => l.priority === "cold").length,
    avgScore:
      leads.length > 0
        ? Math.round(leads.reduce((sum, l) => sum + l.score, 0) / leads.length)
        : 0,
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4 mb-6">
      <div className="bg-white rounded-lg shadow p-6">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm text-gray-600 uppercase tracking-wide">
              Total Leads
            </p>
            <p className="text-3xl font-bold text-gray-900 mt-1">
              {stats.total}
            </p>
          </div>
          <TrendingUp className="w-10 h-10 text-blue-500" />
        </div>
      </div>

      <div className="bg-gradient-to-br from-red-50 to-red-100 rounded-lg shadow p-6">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm text-red-700 uppercase tracking-wide">
              Hot Leads
            </p>
            <p className="text-3xl font-bold text-red-900 mt-1">{stats.hot}</p>
          </div>
          <Flame className="w-10 h-10 text-red-600" />
        </div>
      </div>

      <div className="bg-gradient-to-br from-orange-50 to-orange-100 rounded-lg shadow p-6">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm text-orange-700 uppercase tracking-wide">
              Warm Leads
            </p>
            <p className="text-3xl font-bold text-orange-900 mt-1">
              {stats.warm}
            </p>
          </div>
          <ThermometerSun className="w-10 h-10 text-orange-600" />
        </div>
      </div>

      <div className="bg-gradient-to-br from-blue-50 to-blue-100 rounded-lg shadow p-6">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm text-blue-700 uppercase tracking-wide">
              Cold Leads
            </p>
            <p className="text-3xl font-bold text-blue-900 mt-1">
              {stats.cold}
            </p>
          </div>
          <Snowflake className="w-10 h-10 text-blue-600" />
        </div>
      </div>

      <div className="bg-gradient-to-br from-purple-50 to-purple-100 rounded-lg shadow p-6">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm text-purple-700 uppercase tracking-wide">
              Avg Score
            </p>
            <p className="text-3xl font-bold text-purple-900 mt-1">
              {stats.avgScore}
            </p>
          </div>
          <div className="w-10 h-10 flex items-center justify-center bg-purple-200 rounded-full">
            <span className="text-xl font-bold text-purple-800">%</span>
          </div>
        </div>
      </div>
    </div>
  );
}
