import { CheckCircle2, Circle, Loader2, XCircle } from 'lucide-react'

function AgentProgress({ steps, currentStep }) {
  const getStepIcon = (step) => {
    if (step.status === 'completed') {
      return <CheckCircle2 className="text-success" size={24} />
    } else if (step.status === 'active') {
      return <Loader2 className="text-primary-600 animate-spin" size={24} />
    } else if (step.status === 'error') {
      return <XCircle className="text-error" size={24} />
    } else {
      return <Circle className="text-gray-300" size={24} />
    }
  }

  const getStepClass = (step) => {
    if (step.status === 'completed') return 'agent-step completed'
    if (step.status === 'active') return 'agent-step active'
    if (step.status === 'error') return 'agent-step border-error bg-red-50'
    return 'agent-step'
  }

  return (
    <div className="card">
      <h2 className="text-2xl font-bold text-gray-800 mb-4">
        Agent Pipeline
      </h2>
      <p className="text-sm text-gray-600 mb-6">
        Processing your diagnosis through specialized AI agents
      </p>
      
      <div className="space-y-3">
        {steps.map((step, index) => (
          <div key={step.id} className={getStepClass(step)}>
            <div className="flex items-start gap-3">
              <div className="flex-shrink-0 mt-0.5">
                {getStepIcon(step)}
              </div>
              
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2 mb-1">
                  <span className="text-xs font-semibold text-gray-500">
                    STEP {step.id}/5
                  </span>
                  <span className="text-sm font-bold text-gray-900">
                    {step.name}
                  </span>
                </div>
                
                {step.message && (
                  <p className="text-sm text-gray-600 mb-2">
                    {step.message}
                  </p>
                )}
                
                {step.result && (
                  <div className="mt-2 p-3 bg-gray-50 rounded border border-gray-200">
                    <p className="text-sm text-gray-700 whitespace-pre-wrap">
                      {typeof step.result === 'string' 
                        ? step.result 
                        : JSON.stringify(step.result, null, 2)
                      }
                    </p>
                  </div>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

export default AgentProgress
