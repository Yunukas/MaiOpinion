import { FileText } from 'lucide-react'

function ConditionInput({ condition, setCondition, disabled }) {
  return (
    <div>
      <label className="block text-sm font-semibold text-gray-700 mb-2 flex items-center gap-2">
        <FileText size={16} />
        Patient Condition Description *
      </label>
      <textarea
        value={condition}
        onChange={(e) => setCondition(e.target.value)}
        disabled={disabled}
        placeholder="Describe the symptoms, duration, and any relevant medical history...&#10;&#10;Example: 'Severe tooth pain for 3 days, sensitivity to cold, visible dark spot on upper molar'"
        className="input-field resize-none h-32"
        required
      />
      <p className="mt-2 text-xs text-gray-500">
        Be as specific as possible about symptoms, duration, and affected areas
      </p>
    </div>
  )
}

export default ConditionInput
