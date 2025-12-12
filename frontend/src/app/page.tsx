"use client";

import Link from "next/link";

export default function Home() {
  return (
    <main className="min-h-screen flex items-center justify-center p-4">
      {/* Background effects */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-purple-500/20 rounded-full blur-3xl floating" />
        <div
          className="absolute bottom-1/4 right-1/4 w-80 h-80 bg-cyan-500/20 rounded-full blur-3xl floating"
          style={{ animationDelay: "1.5s" }}
        />
      </div>

      <div className="glass-card p-12 max-w-md w-full text-center relative z-10">
        {/* Logo */}
        <div className="mb-8">
          <div className="w-20 h-20 mx-auto mb-4 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-2xl flex items-center justify-center shadow-lg">
            <svg
              className="w-10 h-10 text-white"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M13 10V3L4 14h7v7l9-11h-7z"
              />
            </svg>
          </div>
          <h1 className="text-3xl font-bold gradient-text mb-2">
            FastAPI Auth
          </h1>
          <p className="text-gray-400">Modern authentication system</p>
        </div>

        {/* Buttons */}
        <div className="space-y-4">
          <Link href="/login" className="block">
            <button className="btn-primary w-full">🔐 로그인</button>
          </Link>

          <Link href="/signup" className="block">
            <button
              className="btn-primary w-full"
              style={{
                background: "linear-gradient(135deg, #06b6d4 0%, #3b82f6 100%)",
              }}
            >
              ✨ 회원가입
            </button>
          </Link>
        </div>

        {/* Divider */}
        <div className="my-8 flex items-center">
          <div className="flex-1 border-t border-gray-700"></div>
          <span className="px-4 text-gray-500 text-sm">FastAPI + Next.js</span>
          <div className="flex-1 border-t border-gray-700"></div>
        </div>

        {/* Features */}
        <div className="grid grid-cols-3 gap-4 text-center text-sm">
          <div>
            <div className="text-2xl mb-1">🔒</div>
            <div className="text-gray-400">JWT 인증</div>
          </div>
          <div>
            <div className="text-2xl mb-1">⚡</div>
            <div className="text-gray-400">FastAPI</div>
          </div>
          <div>
            <div className="text-2xl mb-1">🎨</div>
            <div className="text-gray-400">Next.js</div>
          </div>
        </div>
      </div>
    </main>
  );
}
