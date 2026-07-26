export default function AnalysisCard({ analysis }) {
  return (
    <div className="rounded-xl border bg-white p-6 shadow-sm">
      <h2 className="text-xl font-bold">
        📄 Summary
      </h2>

      <p className="mt-3">
        {analysis.summary}
      </p>

      <h2 className="mt-6 text-xl font-bold">
        ⚠ Risks
      </h2>

      <ul className="list-disc pl-6">
        {analysis.risks.map((risk) => (
          <li key={risk}>{risk}</li>
        ))}
      </ul>

      {/* Render other sections similarly */}
    </div>
  );
}