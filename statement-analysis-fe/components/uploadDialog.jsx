"use client"

import { useState, useRef, useEffect } from "react"
import { FileSpreadsheet, X, ArrowRight, CheckCircle2, Upload, Loader2 } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Dialog, DialogContent, DialogTitle } from "@/components/ui/dialog"
import { VisuallyHidden } from "@/components/ui/visually-hidden"
import { cn } from "@/lib/utils"
import { Spinner } from "@/components/ui/spinner"

export default function UploadDialog({ isUploadOpen, updateUploadState }) {
  const [file, setFile] = useState(null)
  const [isDragging, setIsDragging] = useState(false)
  const [isUploading, setIsUploading] = useState(false)
  const fileInputRef = useRef(null)

  useEffect(() => {
    if (!isUploadOpen) {
      setFile(null)
    }
  }, [isUploadOpen])

  const handleFileDrop = (e) => {
    e.preventDefault()
    setIsDragging(false)

    const droppedFile = e.dataTransfer.files[0]
    if (isValidFile(droppedFile)) {
      setFile(droppedFile)
    } else {
      alert("Please upload a valid Excel file (.xlsx, .xls, or .csv)")
    }
  }

  const handleFileSelect = (e) => {
    const selectedFile = e.target.files?.[0]
    if (selectedFile && isValidFile(selectedFile)) {
      setFile(selectedFile)
    } else {
      alert("Please upload a valid Excel file (.xlsx, .xls, or .csv)")
    }
  }

  const isValidFile = (file) => {
    const validTypes = [
      "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", // xlsx
      "application/vnd.ms-excel", // xls
      "text/csv", // csv
    ]
    return validTypes.includes(file.type)
  }

  const handleUpload = async () => {
    if (!file) return
    setIsUploading(true)
    
    document.body.style.pointerEvents = "none";

    const formData = new FormData()
    formData.append("file", file)

    try {
        const response = await fetch("http://localhost:8001/upload/statement/", {
            method: "POST",
            body: formData,
        })

        if (!response.ok) {
            throw new Error("Failed to upload file")
        }
        setFile(null)
        updateUploadState(false)
        window.location.reload()
    } catch (error) {
        alert(error.message)
    } finally {
        setIsUploading(false);
        document.body.style.pointerEvents = "auto";
    }
  }

  return (
    <>
      {/* Hidden File Input */}
      <input ref={fileInputRef} type="file" accept=".xlsx,.xls,.csv" className="hidden" onChange={handleFileSelect} />

      {/* Upload Dialog */}
      <Dialog open={isUploadOpen} onOpenChange={(state) => {
            if (!isUploading) updateUploadState(state); // Prevent closing when uploading
          }} >
        <DialogContent className="sm:max-w-lg p-0 overflow-hidden dark:bg-gray-950">
          <DialogTitle asChild>
            <VisuallyHidden>Upload Bank Statement</VisuallyHidden>
          </DialogTitle>

          <div className="relative p-6 pb-0">
            <button
              onClick={() => updateUploadState(false)}
              className="absolute right-4 top-4 p-2 rounded-full hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
            >
              <VisuallyHidden>Close</VisuallyHidden>
            </button>
            <div className="flex items-center space-x-3  dark:text-blue-500">
              <FileSpreadsheet className="w-6 h-6 text-green-600" aria-hidden="true" />
              <h2 className="text-xl font-semibold">Upload Statement</h2>
            </div>
            <div className="mt-10 items-center text-black-600 dark:text-black-500">
              Upload your bank statement in Excel format (.xlsx, .xls)
            </div>
          </div>

          <div className="p-6">
            <div
              className={cn(
                "relative group rounded-lg transition-all duration-200",
                isDragging ? "scale-98" : "scale-100",
                file ? "bg-blue-50 dark:bg-blue-950/50" : "bg-gray-50 dark:bg-gray-900",
              )}
            >
              <div
                className={cn(
                  "relative border-2 border-dashed rounded-lg transition-all duration-200",
                  isDragging ? "border-blue-500 scale-98" : "border-gray-300 dark:border-gray-700 scale-100",
                  file
                    ? "border-blue-500 dark:border-blue-600"
                    : "group-hover:border-gray-400 dark:group-hover:border-gray-600",
                )}
                onDragOver={(e) => {
                  e.preventDefault()
                  setIsDragging(true)
                }}
                onDragLeave={(e) => {
                  e.preventDefault()
                  setIsDragging(false)
                }}
                onDrop={handleFileDrop}
              >
                <div className="p-8 text-center">
                  <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-blue-100 dark:bg-blue-900/50 flex items-center justify-center">
                    {file ? (
                      <CheckCircle2 className="w-8 h-8 text-blue-600 dark:text-blue-500" aria-hidden="true" />
                    ) : (
                      <Upload className="w-8 h-8 text-blue-600 dark:text-blue-500" aria-hidden="true" />
                    )}
                  </div>

                  <div className="space-y-2">
                    <p className="text-lg font-medium">{file ? file.name : "Drop your statement here"}</p>
                    <p className="text-sm text-gray-500 dark:text-gray-400">
                      {file ? (
                        "File selected"
                      ) : (
                        <>
                          Drag and drop or <span className="text-black-600 dark:text-blue-500">browse</span>
                        </>
                      )}
                    </p>
                  </div>

                  <div className="mt-6">
                    {file ? (
                      <Button 
                        className="bg-blue-600 hover:bg-blue-700 text-white shadow-lg shadow-blue-500/25 hover:shadow-blue-500/35"
                        onClick={handleUpload}
                        disabled={isUploading}
                      >
                        {
                            isUploading ? (
                                <>
                                    {/* <Loader2 className="w-4 h-4 mr-2 animate-spin" aria-hidden="true" /> */}
                                    <Spinner />
                                    Uploading...
                                </>
                            ) : (
                                <>                               
                                    Process Statement
                                    <ArrowRight className="w-4 h-4 ml-2" aria-hidden="true" />
                                </>
                            )
                        }
                        
                      </Button>
                    ) : (
                      <Button variant="outline" onClick={() => fileInputRef.current?.click()}>
                        Select File
                      </Button>
                    )}
                  </div>
                </div>
              </div>
            </div>

            <div className="mt-4 text-xs text-center text-gray-500 dark:text-gray-400">
              Supported formats: .xlsx, .xls
            </div>
          </div>
        </DialogContent>
      </Dialog>
    </>
  )
}

