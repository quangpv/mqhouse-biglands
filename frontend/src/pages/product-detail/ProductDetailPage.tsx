import { useProductDetailState } from "./facades/useProductDetailState"
import { useReportDeposit } from "./facades/useReportDeposit"
import { useReportClosure } from "./facades/useReportClosure"
import { useReportCancellation } from "./facades/useReportCancellation"
import { useReportSoldOut } from "./facades/useReportSoldOut"
import { ImageGallery } from "./components/ImageGallery"
import { KeyInfoSection } from "./components/KeyInfoSection"
import { AgentContactInfo } from "./components/AgentContactInfo"
import { DealActionButtons } from "./components/DealActionButtons"
import { PropertyFeaturesTable } from "./components/PropertyFeaturesTable"
import { ReviewsSection } from "./components/ReviewsSection"
import { DepositDialog } from "./components/DepositDialog"
import { CancellationDialog } from "./components/CancellationDialog"
import { ClosureDialog } from "./components/ClosureDialog"
import { SoldOutDialog } from "./components/SoldOutDialog"
import { Separator } from "@/shared/components/ui/separator"
import { Badge } from "@/shared/components/ui/badge"
import { PageHeader } from "@/shared/components/page-header"
import { LoadingScreen } from "@/shared/components/loading-screen"
import { ErrorDisplay } from "@/shared/components/error-display"
import { getStatusLabel, getStatusColor } from "@/shared/utils"

export default function ProductDetailPage() {
  const st = useProductDetailState()
  const { mutate: doDeposit, isPending: isDepositing } = useReportDeposit(st.id!)
  const { mutate: doClosure, isPending: isClosing } = useReportClosure(st.id!)
  const { mutate: doCancellation, isPending: isCancelling } = useReportCancellation(st.id!)
  const { mutate: doSoldOut, isPending: isSellingOut } = useReportSoldOut(st.id!)

  if (st.query.isLoading) return <LoadingScreen />
  if (st.query.isError || !st.listing) {
    return (
      <ErrorDisplay
        message="Không thể tải thông tin tin đăng"
        onRetry={() => st.query.refetch()}
      />
    )
  }

  const listing = st.listing

  return (
    <div className="max-w-3xl mx-auto space-y-6">
      <PageHeader
        title={listing.title || listing.address}
        description={`Mã hàng: ${listing.code}`}
      />

      <div className="flex items-center gap-2">
        {listing.is_hot && <Badge className="bg-red-500 text-white">Hot</Badge>}
        <Badge variant="outline">{getStatusLabel(listing.status)}</Badge>
        <span className={`ml-auto h-2.5 w-2.5 rounded-full ${getStatusColor(listing.status)}`} />
      </div>

      <ImageGallery images={listing.images} />
      <KeyInfoSection listing={listing} />

      <Separator />

      <AgentContactInfo
        listing={listing}
        ownerPhoneVisible={st.ownerPhoneVisible}
        onToggleOwnerPhone={() => st.setOwnerPhoneVisible((v) => !v)}
      />

      <Separator />

      <DealActionButtons
        listing={listing}
        isOwner={st.isOwner}
        onDeposit={() => st.openDialog("deposit")}
        onClosure={() => st.openDialog("closure")}
        onCancellation={() => st.openDialog("cancellation")}
        onSoldOut={() => st.openDialog("sold-out")}
      />

      <Separator />

      <div>
        <h3 className="mb-2 font-semibold">Mô tả</h3>
        <p className="whitespace-pre-wrap text-sm text-muted-foreground">{listing.description}</p>
      </div>

      <Separator />

      <PropertyFeaturesTable listing={listing} />

      <Separator />

      <ReviewsSection listingId={listing.id} />

      <DepositDialog
        open={st.activeDialog === "deposit"}
        onClose={st.closeDialog}
        onSubmit={(data) => doDeposit(data, { onSuccess: st.closeDialog })}
        isPending={isDepositing}
      />

      <CancellationDialog
        open={st.activeDialog === "cancellation"}
        onClose={st.closeDialog}
        onSubmit={(data) => doCancellation(data, { onSuccess: st.closeDialog })}
        isPending={isCancelling}
        form={st.cancellationForm}
      />

      <ClosureDialog
        open={st.activeDialog === "closure"}
        onClose={st.closeDialog}
        onSubmit={(notes) => doClosure(notes, { onSuccess: st.closeDialog })}
        isPending={isClosing}
      />

      <SoldOutDialog
        open={st.activeDialog === "sold-out"}
        onClose={st.closeDialog}
        onSubmit={(notes) => doSoldOut(notes, { onSuccess: st.closeDialog })}
        isPending={isSellingOut}
      />
    </div>
  )
}
