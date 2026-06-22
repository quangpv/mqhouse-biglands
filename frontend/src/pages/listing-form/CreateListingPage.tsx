import { useNavigate } from "react-router-dom"
import { Form } from "@/shared/components/ui/form"
import { Button } from "@/shared/components/ui/button"
import { Separator } from "@/shared/components/ui/separator"
import { BasicInfoSection } from "./components/BasicInfoSection"
import { PropertyDetailsSection } from "./components/PropertyDetailsSection"
import { LocationSection } from "./components/LocationSection"
import { CommissionSection } from "./components/CommissionSection"
import { ContactSection } from "./components/ContactSection"
import { ImageUploader } from "./components/ImageUploader"
import { useListingFormState } from "./facades/useListingFormState"
import { useCreateListing } from "./facades/useCreateListing"
import type { IListingForm } from "./types"

export default function CreateListingPage() {
  const navigate = useNavigate()
  const { form, autoCalcTotalArea } = useListingFormState()
  const { mutation, images, setImages } = useCreateListing()

  async function onSubmit(data: IListingForm) {
    mutation.mutate(data)
  }

  return (
    <div className="max-w-3xl mx-auto py-6 space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">Đăng tin mới</h1>
        <Button type="button" variant="ghost" onClick={() => navigate(-1)}>
          Quay lại
        </Button>
      </div>

      <Separator />

      <Form {...form}>
        <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
          <BasicInfoSection form={form} />
          <PropertyDetailsSection form={form} onAreaChange={autoCalcTotalArea} />
          <LocationSection form={form} />
          <CommissionSection form={form} />
          <ContactSection form={form} />
          <ImageUploader images={images} onImagesChange={setImages} />

          <div className="flex items-center justify-end gap-4">
            <Button
              type="button"
              variant="outline"
              onClick={() => navigate(-1)}
              disabled={mutation.isPending}
            >
              Hủy
            </Button>
            <Button type="submit" disabled={mutation.isPending}>
              {mutation.isPending ? "Đang xử lý..." : "Đăng tin"}
            </Button>
          </div>
        </form>
      </Form>
    </div>
  )
}
