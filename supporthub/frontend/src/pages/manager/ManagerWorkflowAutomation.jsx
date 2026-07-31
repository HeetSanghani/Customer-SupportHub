import { CheckCircle2, MessageSquare, Search, Bot, User, ArrowDown } from 'lucide-react'

export default function ManagerWorkflowAutomation() {
  return (
    <div className="flex-1 overflow-auto bg-[#F6F7FC] p-8 text-[#1C1B2E]">
      <div className="mb-8">
        <h1 className="text-2xl font-bold font-['Plus_Jakarta_Sans']">Workflow Automation</h1>
        <p className="text-[#6C7089] text-sm mt-1">How a customer message flows from first contact to a closed, analyzed ticket.</p>
      </div>

      <div className="bg-white p-8 rounded-2xl border border-[#E5E7F3] shadow-sm max-w-3xl mx-auto flex flex-col items-center">
        
        {/* Node 1 */}
        <div className="w-full max-w-md bg-gray-50 border border-gray-200 rounded-xl p-4 flex items-center gap-4">
          <div className="w-10 h-10 rounded-full bg-blue-100 text-blue-600 flex items-center justify-center shrink-0">
            <MessageSquare size={18} />
          </div>
          <div>
            <div className="font-bold text-sm">Customer Message</div>
            <div className="text-xs text-[#6C7089]">Sent via Website Chat or Email</div>
          </div>
        </div>

        <ArrowDown className="text-gray-300 my-2" size={24} />

        {/* Node 2 */}
        <div className="w-full max-w-md bg-gray-50 border border-gray-200 rounded-xl p-4 flex items-center gap-4">
          <div className="w-10 h-10 rounded-full bg-indigo-100 text-indigo-600 flex items-center justify-center shrink-0">
            <Search size={18} />
          </div>
          <div>
            <div className="font-bold text-sm">AI Knowledge Search</div>
            <div className="text-xs text-[#6C7089]">AI scans the Knowledge Base for a relevant answer</div>
          </div>
        </div>

        <ArrowDown className="text-gray-300 my-2" size={24} />

        {/* Node 3 */}
        <div className="w-full max-w-md bg-purple-50 border border-purple-200 rounded-xl p-4 flex items-center gap-4">
          <div className="w-10 h-10 rounded-full bg-purple-100 text-purple-600 flex items-center justify-center shrink-0">
            <Bot size={18} />
          </div>
          <div>
            <div className="font-bold text-sm">AI Reply Generated</div>
            <div className="text-xs text-[#6C7089]">A draft or live answer is generated for the customer</div>
          </div>
        </div>

        <ArrowDown className="text-gray-300 my-2" size={24} />

        {/* Split */}
        <div className="w-full max-w-2xl flex justify-between gap-8 mt-2">
          {/* Left Branch */}
          <div className="flex-1 flex flex-col items-center">
            <div className="text-xs font-bold text-emerald-600 mb-2">High Confidence</div>
            <div className="w-full bg-emerald-50 border border-emerald-200 rounded-xl p-4 flex items-center gap-4">
              <div className="w-10 h-10 rounded-full bg-emerald-100 text-emerald-600 flex items-center justify-center shrink-0">
                <CheckCircle2 size={18} />
              </div>
              <div>
                <div className="font-bold text-sm text-emerald-800">Resolved by AI</div>
                <div className="text-xs text-emerald-600">Ticket closes automatically</div>
              </div>
            </div>
          </div>

          {/* Right Branch */}
          <div className="flex-1 flex flex-col items-center">
            <div className="text-xs font-bold text-orange-600 mb-2">Low Confidence / Complex</div>
            <div className="w-full bg-orange-50 border border-orange-200 rounded-xl p-4 flex items-center gap-4">
              <div className="w-10 h-10 rounded-full bg-orange-100 text-orange-600 flex items-center justify-center shrink-0">
                <User size={18} />
              </div>
              <div>
                <div className="font-bold text-sm text-orange-800">Escalate to Agent</div>
                <div className="text-xs text-orange-600">Routes to a human agent</div>
              </div>
            </div>
          </div>
        </div>

      </div>
    </div>
  )
}
