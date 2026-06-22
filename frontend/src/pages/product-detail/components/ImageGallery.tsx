import { useState } from "react"
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/shared/components/ui/dialog"
import type { ListingImageDTO } from "@/data/types/listing.dto"

interface ImageGalleryProps {
  images: ListingImageDTO[]
}

export function ImageGallery({ images }: ImageGalleryProps) {
  const [selectedIndex, setSelectedIndex] = useState(0)
  const [lightboxOpen, setLightboxOpen] = useState(false)

  if (images.length === 0) {
    return (
      <div className="flex h-64 items-center justify-center rounded-lg bg-muted text-muted-foreground">
        Chưa có hình ảnh
      </div>
    )
  }

  const current = images[selectedIndex]

  return (
    <>
      <div className="space-y-2">
        <div
          className="relative flex h-64 cursor-pointer items-center justify-center overflow-hidden rounded-lg bg-muted"
          onClick={() => setLightboxOpen(true)}
        >
          <img src={current.url} alt="" className="h-full w-full object-contain" />
          <span className="absolute bottom-2 right-2 rounded bg-black/60 px-2 py-0.5 text-xs text-white">
            {selectedIndex + 1}/{images.length}
          </span>
        </div>
        {images.length > 1 && (
          <div className="flex gap-2 overflow-x-auto pb-1">
            {images.map((img, idx) => (
              <button
                key={img.id}
                onClick={() => setSelectedIndex(idx)}
                className={`h-14 w-20 shrink-0 overflow-hidden rounded-md border-2 ${
                  idx === selectedIndex ? "border-primary" : "border-transparent"
                }`}
              >
                <img src={img.url} alt="" className="h-full w-full object-cover" />
              </button>
            ))}
          </div>
        )}
      </div>

      <Dialog open={lightboxOpen} onOpenChange={setLightboxOpen}>
        <DialogContent className="max-w-3xl">
          <DialogHeader>
            <DialogTitle className="sr-only">Hình ảnh</DialogTitle>
          </DialogHeader>
          <div className="flex items-center justify-center">
            <img src={current.url} alt="" className="max-h-[70vh] object-contain" />
          </div>
          <div className="flex items-center justify-center gap-4">
            <button
              onClick={() => setSelectedIndex(Math.max(0, selectedIndex - 1))}
              disabled={selectedIndex === 0}
              className="text-sm disabled:opacity-30"
            >
              ← Trước
            </button>
            <span className="text-sm text-muted-foreground">
              {selectedIndex + 1} / {images.length}
            </span>
            <button
              onClick={() => setSelectedIndex(Math.min(images.length - 1, selectedIndex + 1))}
              disabled={selectedIndex === images.length - 1}
              className="text-sm disabled:opacity-30"
            >
              Sau →
            </button>
          </div>
        </DialogContent>
      </Dialog>
    </>
  )
}
