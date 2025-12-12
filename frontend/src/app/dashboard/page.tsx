"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";

export default function DashboardPage() {
  const router = useRouter();
  const [username, setUsername] = useState<string>("");
  const [token, setToken] = useState<string>("");

  useEffect(() => {
    // JWT에서 username 추출
    const accessToken = localStorage.getItem("access_token");
    if (!accessToken) {
      router.push("/login");
      return;
    }

    setToken(accessToken);

    // JWT 디코딩 (base64)
    try {
      const payload = JSON.parse(atob(accessToken.split(".")[1]));
      setUsername(payload.sub || "User");
    } catch {
      setUsername("User");
    }
  }, [router]);

  const handleLogout = () => {
    localStorage.removeItem("access_token");
    router.push("/");
  };

  return (
    <main className="min-h-screen flex items-center justify-center p-4">
      {/* Background effects */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-green-500/20 rounded-full blur-3xl floating" />
        <div
          className="absolute bottom-1/4 right-1/4 w-80 h-80 bg-emerald-500/20 rounded-full blur-3xl floating"
          style={{ animationDelay: "1.5s" }}
        />
      </div>

      <div className="glass-card p-10 max-w-lg w-full relative z-10">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="w-20 h-20 mx-auto mb-4 bg-gradient-to-br from-green-500 to-emerald-600 rounded-full flex items-center justify-center shadow-lg text-3xl">
            👋
          </div>
          <h1 className="text-3xl font-bold text-white mb-2">
            환영합니다, <span className="gradient-text">{username}</span>!
          </h1>
          <p className="text-gray-400">로그인에 성공했습니다</p>
        </div>

        {/* Token display */}
        <div className="mb-8">
          <label className="block text-sm font-medium text-gray-300 mb-2">
            🔐 JWT Access Token
          </label>
          <div className="bg-gray-900/50 rounded-xl p-4 border border-gray-700">
            <code className="text-xs text-cyan-400 break-all">{token}</code>
          </div>
        </div>

        {/* Token info */}
        <div className="grid grid-cols-2 gap-4 mb-8">
          <div className="bg-gray-900/30 rounded-xl p-4 border border-gray-700">
            <div className="text-gray-400 text-sm mb-1">사용자</div>
            <div className="text-white font-semibold">{username}</div>
          </div>
          <div className="bg-gray-900/30 rounded-xl p-4 border border-gray-700">
            <div className="text-gray-400 text-sm mb-1">상태</div>
            <div className="text-green-400 font-semibold flex items-center gap-1">
              <span className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></span>
              인증됨
            </div>
          </div>
        </div>

        {/* Actions */}
        <div className="space-y-3">
          <button
            onClick={handleLogout}
            className="btn-primary w-full"
            style={{
              background: "linear-gradient(135deg, #ef4444 0%, #dc2626 100%)",
            }}
          >
            🚪 로그아웃
          </button>
          <Link href="/" className="block">
            <button className="w-full py-3 px-6 border border-gray-600 rounded-xl text-gray-300 hover:bg-gray-800/50 transition-colors">
              🏠 홈으로
            </button>
          </Link>
        </div>
      </div>
    </main>
  );
}
