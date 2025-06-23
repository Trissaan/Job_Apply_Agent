'use client'
import { useRef, useState } from 'react'
import axios from '@/lib/api'
import Navbar from '@/components/Navbar'

export default function UploadPage() {
  const inputRef = useRef<HTMLInputElement>(null)
  const [file, setFile] = useState<File | null>(null)
  const [message, setMessage] = useState('')

  const handleUpload = async () => {
    if (!file) {
      setMessage('❌ No file selected.')
      return
    }

    const formData = new FormData()
    formData.append('file', file)

    try {
      const res = await axios.post('/resume/upload-resume', formData)
      setMessage(`✅ Resume uploaded: ${res.data.resume_url}`)
    } catch (err: any) {
      console.error(err)
      setMessage('❌ Upload failed: ' + (err.response?.data?.error || err.message))
    }
  }

  return (
    <div>
      <Navbar />
      <div className="p-6 max-w-xl mx-auto">
        <h1 className="text-xl font-bold mb-4">Upload Resume</h1>

        <input
          type="file"
          ref={inputRef}
          className="block mb-4"
          onChange={(e) => setFile(e.target.files?.[0] || null)}
        />

        <button
          className="bg-blue-600 text-white px-4 py-2 rounded"
          onClick={handleUpload}
        >
          Upload
        </button>

        {message && <p className="mt-4 text-sm">{message}</p>}
      </div>
    </div>
  )
}
