// src/app/login/page.tsx
'use client';

import { SignIn } from '@clerk/nextjs';
import { motion } from 'framer-motion';
import Image from 'next/image';
import { Loader2 } from 'lucide-react';

export default function LoginPage() {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
      className="min-h-screen flex items-center justify-center p-4 bg-gradient-to-br from-background to-muted/20"
    >
      <div className="w-full max-w-2xl flex flex-col items-center">
        {/* 品牌标识区 */}
        <motion.div
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.2 }}
          className="mb-8 text-center space-y-4"
        >
          <div className="relative h-24 w-24 mx-auto">
            <Image
              src="/logo.svg"
              alt="GitToPod Logo"
              fill
              priority
              className="object-contain"
              sizes="(max-width: 768px) 96px, 128px"
            />
          </div>
          <h1 className="text-4xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-primary to-primary/80">
            GitToPod
          </h1>
          <p className="text-lg text-muted-foreground">
            Developer-Focused Audio Platform
          </p>
        </motion.div>

        {/* 登录卡片 */}
        <motion.div
          initial={{ scale: 0.95 }}
          animate={{ scale: 1 }}
          className="w-full max-w-md bg-card/90 backdrop-blur-sm rounded-xl p-8 shadow-xl border border-border/50"
        >
          <SignIn
            path="/login"
            routing="path"
            appearance={{
              variables: {
                colorPrimary: 'hsl(var(--primary))',
                colorText: 'hsl(var(--foreground))',
                colorTextSecondary: 'hsl(var(--muted-foreground))',
                colorBackground: 'hsl(var(--card))',
                borderRadius: 'var(--radius)'
              },
              elements: {
                rootBox: 'w-full',
                card: 'bg-transparent shadow-none gap-y-6',
                headerTitle: 'text-2xl font-bold text-center',
                formFieldInput: 'bg-background focus:ring-2 focus:ring-primary/30',
                formButtonPrimary: 'bg-primary hover:bg-primary/90 text-primary-foreground',
                socialButtonsBlockButton: 'border-border/50 hover:border-primary/50',
                footerActionLink: 'text-primary hover:text-primary/80 transition-colors'
              }
            }}
            afterSignInUrl="/dashboard"
            afterSignUpUrl="/onboarding"
          />
        </motion.div>

        {/* 加载指示器 */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="mt-8 flex items-center gap-2 text-sm text-muted-foreground"
        >
          <Loader2 className="h-4 w-4 animate-spin" />
          <span>安全验证初始化中...</span>
        </motion.div>
      </div>
    </motion.div>
  );
}