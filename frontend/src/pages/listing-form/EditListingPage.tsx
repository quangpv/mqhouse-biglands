import { useParams, useNavigate } from "react-router-dom"
import { useQuery } from "@tanstack/react-query"
import { Form } from "@/shared/components/ui/form"
import { Button } from "@/shared/components/ui/button"
import { Separator } from "@/shared/components/ui/separator"
import { Skeleton } from "@/shared/components/ui/skeleton"
import { listingRepository } from "@/data/repositories/listing.repository"
import { listingQueries } from "@/data/queries/listing.queries"
import { BasicInfoSection } from "./components/BasicInfoSection"
import { PropertyDetailsSection } from "./components/PropertyDetailsSection"
import { LocationSection } from "./components/LocationSection"
import { CommissionSection } from "./components/CommissionSection"
import { ContactSection } from "./components/ContactSection"
import { useListingFormState } from "./facades/useListingFormState"
import { useUpdateListing } from "./facades/useUpdateListing"

export default function EditListingPage() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()

  const listingQuery = useQuery({
    queryKey: listingQueries.detail(id!),
    queryFn: () => listingRepository.get(id!),
    enabled: !!id,
  })

  const listing = listingQuery.data

  const { form, autoCalcTotalArea } = useListingFormState(listing)
  const { mutation } = useUpdateListing(id!)

  async function onSubmit(data: Parameters<typeof mutation.mutate>[0]) {
    mutation.mutate(data)
  }

  if (listingQuery.isLoading) {
    return (
      <div className="max-w-3xl mx-auto py-6 space-y-6">
        <Skeleton className="h-8 w-48" />
        <Skeleton className="h-96 w-full" />
      </div>
    )
  }

  if (!listing) {
    return (
      <div className="max-w-3xl mx-auto py-6">
        <h1 className="text-2xl font-bold mb-4">Không tìm thấy tin đăng</h1>
        <Button onClick={() => navigate("/")}>Về trang chủ</Button>
      </div>
    )
  }

  return (
    <div className="max-w-3xl mx-auto py-6 space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">Chỉnh sửa tin</h1>
        <Button type="button" variant="ghost" onClick={() => navigate(-1)}>
          Quay lại
        </Button>
      </div>

      <Separator />

      <Form {...form}>
        <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
          <BasicInfoSection form={form} isEdit />
          <PropertyDetailsSection form={form} onAreaChange={autoCalcTotalArea} />
          <LocationSection form={form} />
          <CommissionSection form={form} />
          <ContactSection form={form} />

          <div className="flex items-center justify-end gap-4">
            <Button
              type="button"
              variant="outline"
              onClick={() => navigate(-1)}
              disabled={mutation.isPending}
            >
              Hủy
            </Button>
            {listing.status === "DRAFT" && (
              <Button
                type="button"
                variant="secondary"
                disabled={mutation.isPending}
                onClick={form.handleSubmit((data) => mutation.mutate({ ...data, action: "submit" }))}
              >
                {mutation.isPending ? "Đang xử lý..." : "Đăng tin"}
              </Button>
            )}
            <Button type="submit" disabled={mutation.isPending}>
              {mutation.isPending ? "Đang xử lý..." : "Lưu thay đổi"}
            </Button>
          </div>
        </form>
      </Form>
    </div>
  )
}
