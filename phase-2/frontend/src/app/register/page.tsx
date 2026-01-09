"use client";

import { useRouter } from "next/navigation";
import { useAuth } from "@/lib/auth-context";
import AuthForm from "@/components/forms/AuthForm";

export default function RegisterPage() {
  const { register } = useAuth();
  const router = useRouter();

  const handleSubmit = async (data: { email: string; password: string }) => {
    await register(data.email, data.password);
    router.push("/dashboard");
  };

  return <AuthForm type="register" onSubmit={handleSubmit} />;
}
