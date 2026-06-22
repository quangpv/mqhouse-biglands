import { useRef } from "react"
import { Button } from "@/shared/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/shared/components/ui/card"
import { X, Upload } from "lucide-react"

interface Props {
  images: File[]
  onImagesChange: (files: File[]) => void
  disabled?: boolean
}

export function ImageUploader({ images, onImagesChange, disabled }: Props) {
  const inputRef = useRef<HTMLInputElement>(null)

  function handleSelect() {
    inputRef.current?.click()
  }

  function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
    const files = Array.from(e.target.files ?? [])
    const remaining = 20 - images.length
    onImagesChange([...images, ...files.slice(0, remaining)])
    if (inputRef.current) inputRef.current.value = ""
  }

  function removeImage(index: number) {
    onImagesChange(images.filter((_, i) => i !== index))
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Hình ảnh ({images.length}/20)</CardTitle>
      </CardHeader>
      <CardContent>
        <input
          ref={inputRef}
          type="file"
          accept="image/jpeg,image/png,image/webp"
          multiple
          className="hidden"
          onChange={handleChange}
          disabled={disabled}
        />

        <div className="grid grid-cols-4 gap-3 mb-4">
          {images.map((file, i) => (
            <div key={`${file.name}-${i}`} className="relative group aspect-[4/3] rounded-md overflow-hidden border">
              <img
                src={URL.createObjectURL(file)}
                alt={`Preview ${i + 1}`}
                className="w-full h-full object-cover"
              />
              {!disabled && (
                <button
                  type="button"
                  onClick={() => removeImage(i)}
                  className="absolute top-1 right-1 rounded-full bg-black/60 p-1 text-white opacity-0 group-hover:opacity-100 transition-opacity"
                >
                  <X className="h-3 w-3" />
                </button>
              )}
            </div>
          ))}
        </div>

        {images.length < 20 && (
          <Button type="button" variant="outline" onClick={handleSelect} disabled={disabled}>
            <Upload className="h-4 w-4 mr-2" />
            Chọn hình ảnh
          </Button>
        )}
      </CardContent>
    </Card>
  )
}
