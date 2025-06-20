'use client'
import { useEffect } from 'react'
import { useRouter } from 'next/navigation'
import Navbar from '@/components/Navber'

export default function DashboardPage() {
  const router = useRouter()

  useEffect(() => {
    const token = localStorage.getItem('access_token')
    if (!token) {
      router.push('/login')
    }
  }, [])

  return (
    <div>
      <Navbar />
      <div className="p-6">
        <h1 className="text-2xl font-bold">Welcome to your dashboard</h1>
        <p className="mt-2 text-gray-600">You can now manage job preferences, upload your resume, or let the AI apply for jobs.</p>
      </div>
    </div>
  )
}
