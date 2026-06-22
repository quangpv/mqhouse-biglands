import { useState } from "react"
import { useReviewState } from "../facades/useReviewState"
import { useCreateReview } from "../facades/useCreateReview"
import { useDeleteReview } from "../facades/useDeleteReview"
import { useAuthStore } from "@/shared/context/auth-store"
import { Button } from "@/shared/components/ui/button"
import { Textarea } from "@/shared/components/ui/textarea"
import { Input } from "@/shared/components/ui/input"
import { MessageSquare, Trash2, ImagePlus, X } from "lucide-react"
import { formatDateTime } from "@/shared/utils"

interface ReviewsSectionProps {
  listingId: string
}

export function ReviewsSection({ listingId }: ReviewsSectionProps) {
  const { reviews, query } = useReviewState(listingId)
  const { mutate: doCreate, isPending: isCreating } = useCreateReview(listingId)
  const { mutate: doDelete } = useDeleteReview(listingId)
  const { user } = useAuthStore()
  const [content, setContent] = useState("")
  const [images, setImages] = useState<File[]>([])

  const handleSubmit = () => {
    if (!content.trim()) return
    doCreate({ content: content.trim(), images })
    setContent("")
    setImages([])
  }

  const handleImageSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(e.target.files ?? [])
    setImages((prev) => [...prev, ...files].slice(0, 10))
    e.target.value = ""
  }

  const removeImage = (index: number) => {
    setImages((prev) => prev.filter((_, i) => i !== index))
  }

  const isAuthor = (authorId: string) => user?.id === authorId
  const isAdmin = user?.role === "ADMIN"

  return (
    <div className="space-y-4">
      <h3 className="font-semibold">Nhận xét & Đánh giá</h3>

      {query.isLoading ? (
        <p className="text-sm text-muted-foreground">Đang tải...</p>
      ) : reviews.length === 0 ? (
        <div className="flex flex-col items-center justify-center gap-2 rounded-lg border py-10 text-center">
          <MessageSquare className="h-8 w-8 text-muted-foreground" />
          <p className="text-sm text-muted-foreground">Chưa có nhận xét nào</p>
        </div>
      ) : (
        <div className="space-y-3">
          {reviews.map((review) => (
            <div key={review.id} className="rounded-lg border p-4 space-y-2">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <span className="text-sm font-medium">{review.authorName}</span>
                  <span className="text-xs text-muted-foreground">{formatDateTime(review.createdAt)}</span>
                </div>
                {(isAuthor(review.authorId) || isAdmin) && (
                  <Button
                    variant="ghost"
                    size="icon"
                    className="h-6 w-6"
                    onClick={() => doDelete(review.id)}
                  >
                    <Trash2 className="h-3 w-3 text-destructive" />
                  </Button>
                )}
              </div>
              <p className="text-sm whitespace-pre-wrap">{review.content}</p>
              {review.images.length > 0 && (
                <div className="flex gap-2 flex-wrap">
                  {review.images.map((img) => (
                    <img
                      key={img.id}
                      src={img.url}
                      alt=""
                      className="h-20 w-20 object-cover rounded-md"
                    />
                  ))}
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      <div className="rounded-lg border p-4 space-y-3">
        <Textarea
          placeholder="Viết nhận xét..."
          value={content}
          onChange={(e) => setContent(e.target.value)}
          rows={3}
        />
        {images.length > 0 && (
          <div className="flex gap-2 flex-wrap">
            {images.map((file, i) => (
              <div key={i} className="relative">
                <img
                  src={URL.createObjectURL(file)}
                  alt=""
                  className="h-16 w-16 object-cover rounded-md"
                />
                <button
                  onClick={() => removeImage(i)}
                  className="absolute -top-1 -right-1 bg-destructive text-destructive-foreground rounded-full h-5 w-5 flex items-center justify-center"
                >
                  <X className="h-3 w-3" />
                </button>
              </div>
            ))}
          </div>
        )}
        <div className="flex items-center gap-2">
          <Label htmlFor="review-images" className="cursor-pointer">
            <div className="flex items-center gap-1 text-sm text-muted-foreground hover:text-foreground">
              <ImagePlus className="h-4 w-4" />
              Thêm hình ảnh
            </div>
            <input
              id="review-images"
              type="file"
              accept="image/*"
              multiple
              className="hidden"
              onChange={handleImageSelect}
            />
          </Label>
          <Button
            size="sm"
            onClick={handleSubmit}
            disabled={!content.trim() || isCreating}
            className="ml-auto"
          >
            {isCreating ? "Đang gửi..." : "Gửi đánh giá"}
          </Button>
        </div>
      </div>
    </div>
  )
}

function Label({ children, htmlFor, className }: { children: React.ReactNode; htmlFor: string; className?: string }) {
  return (
    <label htmlFor={htmlFor} className={className}>
      {children}
    </label>
  )
}
