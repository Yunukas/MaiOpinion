import { useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import { Upload, X, Image as ImageIcon } from 'lucide-react'

function ImageUpload({ image, setImage, disabled }) {
  const onDrop = useCallback((acceptedFiles) => {
    if (acceptedFiles && acceptedFiles.length > 0) {
      setImage(acceptedFiles[0])
    }
  }, [setImage])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.png', '.jpg', '.jpeg', '.gif', '.bmp']
    },
    multiple: false,
    disabled
  })

  const removeImage = () => {
    setImage(null)
  }

  return (
    <div>
      <label className="block text-sm font-semibold text-gray-700 mb-2">
        Medical Image *
      </label>
      
      {!image ? (
        <div
          {...getRootProps()}
          className={`
            border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors
            ${isDragActive 
              ? 'border-primary-500 bg-primary-50' 
              : 'border-gray-300 hover:border-primary-400 hover:bg-gray-50'
            }
            ${disabled ? 'opacity-50 cursor-not-allowed' : ''}
          `}
        >
          <input {...getInputProps()} />
          <Upload className="mx-auto h-12 w-12 text-gray-400 mb-3" />
          {isDragActive ? (
            <p className="text-primary-600 font-medium">Drop the image here</p>
          ) : (
            <>
              <p className="text-gray-600 font-medium mb-1">
                Drag & drop a medical image here
              </p>
              <p className="text-sm text-gray-500">
                or click to browse (PNG, JPG, GIF, BMP)
              </p>
            </>
          )}
        </div>
      ) : (
        <div className="relative border-2 border-gray-300 rounded-lg p-4">
          <button
            type="button"
            onClick={removeImage}
            disabled={disabled}
            className="absolute top-2 right-2 bg-red-500 hover:bg-red-600 text-white rounded-full p-1 transition-colors disabled:opacity-50"
          >
            <X size={20} />
          </button>
          
          <div className="flex items-center gap-4">
            <div className="flex-shrink-0 bg-gray-100 rounded-lg p-3">
              <ImageIcon className="text-gray-600" size={32} />
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium text-gray-900 truncate">
                {image.name}
              </p>
              <p className="text-sm text-gray-500">
                {(image.size / 1024).toFixed(1)} KB
              </p>
            </div>
          </div>
          
          {image.type.startsWith('image/') && (
            <div className="mt-4">
              <img
                src={URL.createObjectURL(image)}
                alt="Preview"
                className="max-h-48 mx-auto rounded-lg border border-gray-200"
              />
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default ImageUpload
