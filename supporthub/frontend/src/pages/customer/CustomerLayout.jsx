import { useState } from 'react'
import { Routes, Route, Navigate, useLocation } from 'react-router-dom'
import { useAuthStore } from '../../store/authStore'
import CustomerHeader from '../../components/CustomerHeader'

import ConversationalHome from './ConversationalHome'
import CustomerOrders from './CustomerOrders'
import CustomerShipments from './CustomerShipments'
import CustomerReturnsRefunds from './CustomerReturnsRefunds'
import CustomerSecuritySettings from './CustomerSecuritySettings'
import CustomerProfile from './CustomerProfile'
import CustomerReviews from './CustomerReviews'
import CustomerHelpCenter from './CustomerHelpCenter'

import ContactEmailModal from '../../components/ContactEmailModal'
import ContactWhatsAppModal from '../../components/ContactWhatsAppModal'
import ContactInstagramModal from '../../components/ContactInstagramModal'

export default function CustomerLayout() {
  const { role, isAuthenticated } = useAuthStore()
  const [isEmailModalOpen, setIsEmailModalOpen] = useState(false)
  const [isWhatsAppModalOpen, setIsWhatsAppModalOpen] = useState(false)
  const [isInstagramModalOpen, setIsInstagramModalOpen] = useState(false)

  if (!isAuthenticated || role !== 'customer') return <Navigate to="/login" replace />

  return (
    <div className="flex flex-col h-screen bg-[#F8FAFC] overflow-hidden">
      {/* Clean Compact Top Header */}
      <CustomerHeader
        onOpenWhatsApp={() => setIsWhatsAppModalOpen(true)}
        onOpenInstagram={() => setIsInstagramModalOpen(true)}
        onOpenEmail={() => setIsEmailModalOpen(true)}
      />

      {/* Main Workspace (Takes full height below header) */}
      <main className="flex-1 flex flex-col min-w-0 h-[calc(100vh-4rem)] overflow-hidden">
        <Routes>
          <Route path="/" element={<ConversationalHome />} />
          <Route path="/chat" element={<ConversationalHome />} />
          <Route path="/chat/:id" element={<ConversationalHome />} />
          <Route path="/orders" element={<CustomerOrders />} />
          <Route path="/shipments" element={<CustomerShipments />} />
          <Route path="/returns" element={<CustomerReturnsRefunds />} />
          <Route path="/profile" element={<CustomerProfile />} />
          <Route path="/settings" element={<CustomerSecuritySettings />} />
          <Route path="/help" element={<CustomerHelpCenter />} />
          <Route path="/reviews" element={<CustomerReviews />} />
          <Route path="*" element={<Navigate to="/customer" replace />} />
        </Routes>
      </main>

      {/* Direct Communication Modals */}
      <ContactEmailModal isOpen={isEmailModalOpen} onClose={() => setIsEmailModalOpen(false)} />
      <ContactWhatsAppModal isOpen={isWhatsAppModalOpen} onClose={() => setIsWhatsAppModalOpen(false)} />
      <ContactInstagramModal isOpen={isInstagramModalOpen} onClose={() => setIsInstagramModalOpen(false)} />
    </div>
  )
}
