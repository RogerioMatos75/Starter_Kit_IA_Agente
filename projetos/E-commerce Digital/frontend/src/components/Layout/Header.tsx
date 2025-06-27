'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import Image from 'next/image';
import { useRouter } from 'next/navigation';
import {
  ShoppingCartIcon,
  UserIcon,
  MagnifyingGlassIcon,
  Bars3Icon,
  XMarkIcon,
  HeartIcon,
} from '@heroicons/react/24/outline';
import { useCartStore } from '@/store/cartStore';
import { useAuthStore } from '@/store/authStore';
import { CartDropdown } from '@/components/Cart/CartDropdown';
import { SearchBar } from '@/components/Search/SearchBar';

const navigation = [
  { name: 'Início', href: '/' },
  { name: 'Produtos', href: '/products' },
  { name: 'Categorias', href: '/categories' },
  { name: 'Ofertas', href: '/deals' },
  { name: 'Contato', href: '/contact' },
];

export function Header() {
  const router = useRouter();
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [isCartOpen, setIsCartOpen] = useState(false);
  const [isSearchOpen, setIsSearchOpen] = useState(false);
  
  const { items, getTotalItems } = useCartStore();
  const { user, isAuthenticated, logout } = useAuthStore();
  
  const totalItems = getTotalItems();

  const handleLogout = () => {
    logout();
    router.push('/');
  };

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  const closeMenu = () => {
    setIsMenuOpen(false);
  };

  // Close mobile menu when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      const target = event.target as HTMLElement;
      if (isMenuOpen && !target.closest('.mobile-menu') && !target.closest('.menu-button')) {
        setIsMenuOpen(false);
      }
    };

    document.addEventListener('click', handleClickOutside);
    return () => document.removeEventListener('click', handleClickOutside);
  }, [isMenuOpen]);

  return (
    <header className="bg-white shadow-lg sticky top-0 z-50">
      {/* Top Bar */}
      <div className="bg-primary-600 text-white text-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-2">
            <div className="flex items-center space-x-4">
              <span>📞 (11) 99999-9999</span>
              <span>✉️ contato@ecommerce.com</span>
            </div>
            <div className="hidden md:flex items-center space-x-4">
              <span>🚚 Frete grátis acima de R$ 199</span>
              <span>🔒 Compra 100% segura</span>
            </div>
          </div>
        </div>
      </div>

      {/* Main Header */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center py-4">
          {/* Logo */}
          <div className="flex items-center">
            <Link href="/" className="flex items-center space-x-2">
              <div className="w-10 h-10 bg-primary-600 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-xl">E</span>
              </div>
              <div className="hidden sm:block">
                <h1 className="text-xl font-bold text-gray-900">E-commerce</h1>
                <p className="text-xs text-gray-500">Digital Store</p>
              </div>
            </Link>
          </div>

          {/* Search Bar - Desktop */}
          <div className="hidden lg:block flex-1 max-w-2xl mx-8">
            <SearchBar />
          </div>

          {/* Actions */}
          <div className="flex items-center space-x-4">
            {/* Search Button - Mobile */}
            <button
              onClick={() => setIsSearchOpen(!isSearchOpen)}
              className="lg:hidden p-2 text-gray-600 hover:text-gray-900 transition-colors"
            >
              <MagnifyingGlassIcon className="h-6 w-6" />
            </button>

            {/* Wishlist */}
            <Link
              href="/wishlist"
              className="p-2 text-gray-600 hover:text-gray-900 transition-colors relative"
            >
              <HeartIcon className="h-6 w-6" />
              <span className="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full h-5 w-5 flex items-center justify-center">
                0
              </span>
            </Link>

            {/* Cart */}
            <div className="relative">
              <button
                onClick={() => setIsCartOpen(!isCartOpen)}
                className="p-2 text-gray-600 hover:text-gray-900 transition-colors relative"
              >
                <ShoppingCartIcon className="h-6 w-6" />
                {totalItems > 0 && (
                  <span className="absolute -top-1 -right-1 bg-primary-600 text-white text-xs rounded-full h-5 w-5 flex items-center justify-center">
                    {totalItems}
                  </span>
                )}
              </button>
              {isCartOpen && (
                <CartDropdown onClose={() => setIsCartOpen(false)} />
              )}
            </div>

            {/* User Menu */}
            <div className="relative">
              {isAuthenticated ? (
                <div className="flex items-center space-x-2">
                  <Link
                    href="/account"
                    className="hidden sm:flex items-center space-x-2 text-gray-700 hover:text-gray-900"
                  >
                    <UserIcon className="h-6 w-6" />
                    <span className="text-sm font-medium">{user?.name}</span>
                  </Link>
                  <button
                    onClick={handleLogout}
                    className="text-sm text-gray-500 hover:text-gray-700"
                  >
                    Sair
                  </button>
                </div>
              ) : (
                <div className="flex items-center space-x-2">
                  <Link
                    href="/login"
                    className="text-sm text-gray-700 hover:text-gray-900"
                  >
                    Entrar
                  </Link>
                  <span className="text-gray-300">|</span>
                  <Link
                    href="/register"
                    className="text-sm text-primary-600 hover:text-primary-700 font-medium"
                  >
                    Cadastrar
                  </Link>
                </div>
              )}
            </div>

            {/* Mobile Menu Button */}
            <button
              onClick={toggleMenu}
              className="lg:hidden menu-button p-2 text-gray-600 hover:text-gray-900 transition-colors"
            >
              {isMenuOpen ? (
                <XMarkIcon className="h-6 w-6" />
              ) : (
                <Bars3Icon className="h-6 w-6" />
              )}
            </button>
          </div>
        </div>

        {/* Mobile Search */}
        {isSearchOpen && (
          <div className="lg:hidden pb-4">
            <SearchBar />
          </div>
        )}
      </div>

      {/* Navigation */}
      <nav className="bg-gray-50 border-t border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="hidden lg:flex space-x-8 py-3">
            {navigation.map((item) => (
              <Link
                key={item.name}
                href={item.href}
                className="text-gray-700 hover:text-primary-600 px-3 py-2 text-sm font-medium transition-colors"
              >
                {item.name}
              </Link>
            ))}
          </div>
        </div>
      </nav>

      {/* Mobile Menu */}
      {isMenuOpen && (
        <div className="lg:hidden mobile-menu">
          <div className="px-2 pt-2 pb-3 space-y-1 bg-white border-t border-gray-200 shadow-lg">
            {navigation.map((item) => (
              <Link
                key={item.name}
                href={item.href}
                onClick={closeMenu}
                className="block px-3 py-2 text-base font-medium text-gray-700 hover:text-primary-600 hover:bg-gray-50 rounded-md transition-colors"
              >
                {item.name}
              </Link>
            ))}
            
            {/* Mobile User Actions */}
            <div className="border-t border-gray-200 pt-4 mt-4">
              {isAuthenticated ? (
                <div className="space-y-2">
                  <Link
                    href="/account"
                    onClick={closeMenu}
                    className="block px-3 py-2 text-base font-medium text-gray-700 hover:text-primary-600 hover:bg-gray-50 rounded-md"
                  >
                    Minha Conta
                  </Link>
                  <Link
                    href="/orders"
                    onClick={closeMenu}
                    className="block px-3 py-2 text-base font-medium text-gray-700 hover:text-primary-600 hover:bg-gray-50 rounded-md"
                  >
                    Meus Pedidos
                  </Link>
                  <button
                    onClick={() => {
                      handleLogout();
                      closeMenu();
                    }}
                    className="block w-full text-left px-3 py-2 text-base font-medium text-gray-700 hover:text-primary-600 hover:bg-gray-50 rounded-md"
                  >
                    Sair
                  </button>
                </div>
              ) : (
                <div className="space-y-2">
                  <Link
                    href="/login"
                    onClick={closeMenu}
                    className="block px-3 py-2 text-base font-medium text-gray-700 hover:text-primary-600 hover:bg-gray-50 rounded-md"
                  >
                    Entrar
                  </Link>
                  <Link
                    href="/register"
                    onClick={closeMenu}
                    className="block px-3 py-2 text-base font-medium text-primary-600 hover:text-primary-700 hover:bg-gray-50 rounded-md"
                  >
                    Cadastrar
                  </Link>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </header>
  );
}