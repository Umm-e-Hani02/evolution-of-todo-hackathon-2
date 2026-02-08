"use client";

import { useRouter } from "next/navigation";
import { useAuth } from "@/lib/auth-context";
import AuthForm from "@/components/forms/AuthForm";

export default function LoginPage() {
  const { login } = useAuth();
  const router = useRouter();

  const handleSubmit = async (data: { email: string; password: string }) => {
    await login(data.email, data.password);
    router.push("/dashboard");
  };

  return <AuthForm type="login" onSubmit={handleSubmit} />;
}
