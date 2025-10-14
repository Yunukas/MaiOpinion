import { Heart } from 'lucide-react'

function Header() {
  return (
    <header className="bg-white shadow-sm border-b border-gray-200">
      <div className="container mx-auto px-4 py-6">
        <div className="flex items-center gap-3">
          <div className="bg-primary-600 p-2 rounded-lg">
            <Heart className="text-white" size={32} />
          </div>
          <div>
            <h1 className="text-3xl font-bold text-gray-900">
              MaiOpinion
            </h1>
            <p className="text-sm text-gray-600">
              Multi-Agent AI Healthcare Diagnostic Assistant
            </p>
          </div>
        </div>
      </div>
    </header>
  )
}

export default Header
