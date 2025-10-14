import { useState } from 'react'
import ImageUpload from './components/ImageUpload'
import ConditionInput from './components/ConditionInput'
import EmailInput from './components/EmailInput'
import AgentProgress from './components/AgentProgress'
import DiagnosticReport from './components/DiagnosticReport'
import Header from './components/Header'
import { Activity } from 'lucide-react'

function App() {
  const [image, setImage] = useState(null)
  const [condition, setCondition] = useState('')
  const [wantsEmail, setWantsEmail] = useState(false)
  const [email, setEmail] = useState('')
  const [isProcessing, setIsProcessing] = useState(false)
  const [agentSteps, setAgentSteps] = useState([])
  const [currentStep, setCurrentStep] = useState(null)
  const [finalReport, setFinalReport] = useState(null)
  const [error, setError] = useState(null)

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    if (!image || !condition.trim()) {
      setError('Please upload an image and describe the condition')
      return
    }

    if (wantsEmail && !email.trim()) {
      setError('Please enter your email address')
      return
    }

    setError(null)
    setIsProcessing(true)
    setFinalReport(null)
    
    // Initialize agent steps
    const steps = [
      { id: 1, name: 'Image Detection', status: 'pending', message: '' },
      { id: 2, name: 'Specialized Diagnosis', status: 'pending', message: '' },
      { id: 3, name: 'Clinical Reasoning', status: 'pending', message: '' },
      { id: 4, name: 'Treatment Planning', status: 'pending', message: '' },
      { id: 5, name: 'Follow-Up Care', status: 'pending', message: '' }
    ]
    setAgentSteps(steps)
    setCurrentStep(1)

    try {
      const formData = new FormData()
      formData.append('image', image)
      formData.append('condition', condition)
      if (wantsEmail && email) {
        formData.append('email', email)
      }

      const response = await fetch('/api/diagnose', {
        method: 'POST',
        body: formData
      })

      if (!response.ok) {
        throw new Error('Failed to process diagnosis')
      }

      const reader = response.body.getReader()
      const decoder = new TextDecoder()

      while (true) {
        const { done, value } = await reader.read()
        if (done) break

        const chunk = decoder.decode(value)
        const lines = chunk.split('\n')

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const data = JSON.parse(line.slice(6))
            
            if (data.type === 'step_start') {
              setCurrentStep(data.step)
              setAgentSteps(prev => prev.map(s => 
                s.id === data.step 
                  ? { ...s, status: 'active', message: data.message }
                  : s
              ))
            } else if (data.type === 'step_complete') {
              setAgentSteps(prev => prev.map(s => 
                s.id === data.step 
                  ? { ...s, status: 'completed', message: data.message, result: data.result }
                  : s
              ))
            } else if (data.type === 'complete') {
              setFinalReport(data.report)
              setCurrentStep(null)
            } else if (data.type === 'error') {
              throw new Error(data.message)
            }
          }
        }
      }
    } catch (err) {
      setError(err.message || 'An error occurred during processing')
      setAgentSteps(prev => prev.map(s => 
        s.status === 'active' ? { ...s, status: 'error' } : s
      ))
    } finally {
      setIsProcessing(false)
    }
  }

  const handleReset = () => {
    setImage(null)
    setCondition('')
    setWantsEmail(false)
    setEmail('')
    setAgentSteps([])
    setCurrentStep(null)
    setFinalReport(null)
    setError(null)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <Header />
      
      <main className="container mx-auto px-4 py-8 max-w-7xl">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Left Column - Input Form */}
          <div className="space-y-6">
            <div className="card">
              <h2 className="text-2xl font-bold text-gray-800 mb-6 flex items-center gap-2">
                <Activity className="text-primary-600" />
                Patient Information
              </h2>
              
              <form onSubmit={handleSubmit} className="space-y-6">
                <ImageUpload 
                  image={image} 
                  setImage={setImage}
                  disabled={isProcessing}
                />
                
                <ConditionInput 
                  condition={condition}
                  setCondition={setCondition}
                  disabled={isProcessing}
                />
                
                <div className="border-t pt-6">
                  <label className="flex items-center gap-3 cursor-pointer">
                    <input
                      type="checkbox"
                      checked={wantsEmail}
                      onChange={(e) => setWantsEmail(e.target.checked)}
                      disabled={isProcessing}
                      className="w-5 h-5 text-primary-600 rounded focus:ring-2 focus:ring-primary-500"
                    />
                    <span className="text-gray-700 font-medium">
                      I want to receive follow-up reminders via email
                    </span>
                  </label>
                  
                  {wantsEmail && (
                    <div className="mt-4">
                      <EmailInput 
                        email={email}
                        setEmail={setEmail}
                        disabled={isProcessing}
                      />
                    </div>
                  )}
                </div>

                {error && (
                  <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
                    <p className="font-medium">Error</p>
                    <p className="text-sm">{error}</p>
                  </div>
                )}

                <div className="flex gap-4">
                  <button
                    type="submit"
                    disabled={isProcessing || !image || !condition.trim()}
                    className="btn-primary flex-1"
                  >
                    {isProcessing ? (
                      <span className="flex items-center justify-center gap-2">
                        <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                        </svg>
                        Processing...
                      </span>
                    ) : (
                      'Start Diagnosis'
                    )}
                  </button>
                  
                  {finalReport && (
                    <button
                      type="button"
                      onClick={handleReset}
                      className="btn-secondary"
                    >
                      New Diagnosis
                    </button>
                  )}
                </div>
              </form>
            </div>
          </div>

          {/* Right Column - Results */}
          <div className="space-y-6">
            {agentSteps.length > 0 && (
              <AgentProgress 
                steps={agentSteps}
                currentStep={currentStep}
              />
            )}

            {finalReport && (
              <DiagnosticReport report={finalReport} />
            )}

            {!agentSteps.length && !finalReport && (
              <div className="card text-center py-12">
                <Activity className="mx-auto h-16 w-16 text-gray-300 mb-4" />
                <h3 className="text-xl font-semibold text-gray-500 mb-2">
                  Ready to Diagnose
                </h3>
                <p className="text-gray-400">
                  Upload a medical image and describe the condition to begin
                </p>
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  )
}

export default App
