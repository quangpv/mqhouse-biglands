import { useForm, type Resolver } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { listingFormSchema, type IListingForm } from "../types"
import { listingToFormValues } from "../types"
import type { ListingDTO } from "@/data/types/listing.dto"

export function useListingFormState(existingListing?: ListingDTO | null) {
  const defaultValues: IListingForm = existingListing
    ? listingToFormValues(existingListing)
    : {
        transactionType: "BAN",
        propertyType: "",
        title: undefined,
        description: "",
        price: 0,
        commissionType: "PERCENTAGE",
        commissionValue: 0,
        areaWidth: 0,
        areaLength: 0,
        totalArea: 0,
        numRooms: undefined,
        numBathrooms: undefined,
        numFloors: undefined,
        streetName: "",
        houseNumber: "",
        address: "",
        ward: "",
        district: "",
        city: "",
        latitude: undefined,
        longitude: undefined,
        label: undefined,
        furnishing: undefined,
        frontageType: undefined,
        legalStatus: undefined,
        direction: undefined,
        roadWidth: undefined,
        ownerPhone: "",
        videoUrl: undefined,
      }

  const form = useForm<IListingForm>({
    resolver: zodResolver(listingFormSchema) as unknown as Resolver<IListingForm>,
    defaultValues,
    mode: "onSubmit",
  })

  function resetToDefaults() {
    form.reset(defaultValues)
  }

  function autoCalcTotalArea() {
    const width = form.watch("areaWidth")
    const length = form.watch("areaLength")
    if (width > 0 && length > 0) {
      form.setValue("totalArea", width * length)
    }
  }

  return { form, resetToDefaults, autoCalcTotalArea }
}
