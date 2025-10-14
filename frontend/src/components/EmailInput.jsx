import { Mail } from 'lucide-react'

function EmailInput({ email, setEmail, disabled }) {
  return (
    <div>
      <label className="block text-sm font-semibold text-gray-700 mb-2 flex items-center gap-2">
        <Mail size={16} />
        Email Address
      </label>
      <input
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        disabled={disabled}
        placeholder="your.email@example.com"
        className="input-field"
        required
      />
      <p className="mt-2 text-xs text-gray-500">
        We'll send you follow-up reminders based on your treatment timeline
      </p>
    </div>
  )
}

export default EmailInput
