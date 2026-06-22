export interface ILoginForm {
  username: string
  password: string
}

export interface IForgotPasswordForm {
  username: string
}

export interface IResetPasswordForm {
  newPassword: string
  confirmPassword: string
}
