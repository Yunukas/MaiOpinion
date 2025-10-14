import { FileText, Stethoscope, Pill, Calendar, Download } from 'lucide-react'

function DiagnosticReport({ report }) {
  const downloadReport = () => {
    const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(report, null, 2))
    const downloadAnchor = document.createElement('a')
    downloadAnchor.setAttribute("href", dataStr)
    downloadAnchor.setAttribute("download", `diagnostic_report_${Date.now()}.json`)
    document.body.appendChild(downloadAnchor)
    downloadAnchor.click()
    downloadAnchor.remove()
  }

  return (
    <div className="card">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold text-gray-800 flex items-center gap-2">
          <FileText className="text-primary-600" />
          Diagnostic Report
        </h2>
        <button
          onClick={downloadReport}
          className="flex items-center gap-2 text-sm text-primary-600 hover:text-primary-700 font-medium"
        >
          <Download size={16} />
          Download JSON
        </button>
      </div>

      <div className="space-y-6">
        {/* Image Detection Info */}
        {report.image_type && (
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <h3 className="text-sm font-bold text-blue-900 mb-3 uppercase">
              🔍 Image Detection
            </h3>
            <div className="grid grid-cols-2 gap-3 text-sm">
              <div>
                <p className="text-blue-700 font-medium">Image Type:</p>
                <p className="text-blue-900 font-semibold capitalize">{report.image_type}</p>
              </div>
              <div>
                <p className="text-blue-700 font-medium">Body Part:</p>
                <p className="text-blue-900 font-semibold">{report.body_part}</p>
              </div>
              <div>
                <p className="text-blue-700 font-medium">Modality:</p>
                <p className="text-blue-900 font-semibold">{report.imaging_modality}</p>
              </div>
              <div>
                <p className="text-blue-700 font-medium">Confidence:</p>
                <p className="text-blue-900 font-semibold uppercase">{report.detection_confidence}</p>
              </div>
            </div>
          </div>
        )}

        {/* Findings */}
        {report.finding && (
          <div className="border-l-4 border-yellow-500 pl-4">
            <h3 className="text-sm font-bold text-gray-700 mb-2 flex items-center gap-2 uppercase">
              <FileText size={16} />
              Findings
            </h3>
            <p className="text-gray-800 leading-relaxed">{report.finding}</p>
          </div>
        )}

        {/* Diagnosis */}
        {report.diagnosis && (
          <div className="bg-green-50 border border-green-200 rounded-lg p-4">
            <h3 className="text-sm font-bold text-green-900 mb-2 flex items-center gap-2 uppercase">
              <Stethoscope size={16} />
              Diagnosis
            </h3>
            <p className="text-lg font-bold text-green-900 mb-2">{report.diagnosis}</p>
            {report.confidence && (
              <div className="inline-block bg-green-100 px-3 py-1 rounded-full">
                <p className="text-sm font-semibold text-green-800">
                  Confidence: {report.confidence.toUpperCase()}
                </p>
              </div>
            )}
          </div>
        )}

        {/* Treatment */}
        {report.treatment && (
          <div className="border-l-4 border-purple-500 pl-4">
            <h3 className="text-sm font-bold text-gray-700 mb-3 flex items-center gap-2 uppercase">
              <Pill size={16} />
              Treatment Plan
            </h3>
            <p className="text-gray-800 leading-relaxed mb-3">{report.treatment}</p>
            
            {report.precautions && report.precautions.length > 0 && (
              <div className="mt-4">
                <p className="text-sm font-semibold text-gray-700 mb-2">Precautions:</p>
                <ul className="list-disc list-inside space-y-1">
                  {report.precautions.map((precaution, index) => (
                    <li key={index} className="text-sm text-gray-700">
                      {precaution}
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}

        {/* Follow-Up */}
        {report.follow_up && (
          <div className="bg-orange-50 border border-orange-200 rounded-lg p-4">
            <h3 className="text-sm font-bold text-orange-900 mb-3 flex items-center gap-2 uppercase">
              <Calendar size={16} />
              Follow-Up Care
            </h3>
            
            {report.timeline && (
              <div className="mb-3">
                <span className="inline-block bg-orange-100 px-3 py-1 rounded-full text-sm font-semibold text-orange-800">
                  Timeline: {report.timeline}
                </span>
              </div>
            )}
            
            <p className="text-gray-800 leading-relaxed mb-3">{report.follow_up}</p>
            
            {report.patient_instructions && (
              <div className="mt-3 p-3 bg-white rounded border border-orange-200">
                <p className="text-sm font-semibold text-gray-700 mb-2">
                  Patient Instructions:
                </p>
                <p className="text-sm text-gray-700 leading-relaxed">
                  {report.patient_instructions}
                </p>
              </div>
            )}
          </div>
        )}

        {/* Metadata */}
        <div className="pt-4 border-t border-gray-200">
          <div className="grid grid-cols-2 gap-4 text-xs text-gray-500">
            <div>
              <p className="font-medium">Image Analyzed:</p>
              <p>{report.image_analyzed}</p>
            </div>
            <div>
              <p className="font-medium">Timestamp:</p>
              <p>{new Date(report.timestamp).toLocaleString()}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default DiagnosticReport
