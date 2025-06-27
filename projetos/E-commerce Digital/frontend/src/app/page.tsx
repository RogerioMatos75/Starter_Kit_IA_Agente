'use client';

import { useState, useEffect } from 'react';
import Image from 'next/image';
import Link from 'next/link';
import { ShoppingCartIcon, HeartIcon, StarIcon } from '@heroicons/react/24/outline';
import { StarIcon as StarSolidIcon } from '@heroicons/react/24/solid';
import { useCartStore } from '@/store/cartStore';
import { Product } from '@/types';
import { api } from '@/lib/api';
import toast from 'react-hot-toast';

const featuredProducts: Product[] = [
  {
    id: '1',
    name: 'Smartphone Premium XZ',
    description: 'Smartphone com câmera de 108MP, 256GB de armazenamento e tela AMOLED de 6.7"',
    price: 2499.99,
    image: 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=500',
    category: 'Eletrônicos',
    stock: 15,
    rating: 4.8,
    reviews: 124
  },
  {
    id: '2',
    name: 'Notebook Gamer Ultra',
    description: 'Notebook gamer com RTX 4060, Intel i7, 16GB RAM e SSD 1TB',
    price: 4999.99,
    image: 'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=500',
    category: 'Informática',
    stock: 8,
    rating: 4.9,
    reviews: 89
  },
  {
    id: '3',
    name: 'Fone Bluetooth Premium',
    description: 'Fone de ouvido com cancelamento de ruído ativo e 30h de bateria',
    price: 899.99,
    image: 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500',
    category: 'Áudio',
    stock: 25,
    rating: 4.7,
    reviews: 203
  },
  {
    id: '4',
    name: 'Smart TV 65" 4K',
    description: 'Smart TV LED 65 polegadas 4K Ultra HD com HDR e sistema Android TV',
    price: 3299.99,
    image: 'https://images.unsplash.com/photo-1593359677879-a4bb92f829d1?w=500',
    category: 'TV & Áudio',
    stock: 12,
    rating: 4.6,
    reviews: 156
  }
];

const categories = [
  { name: 'Eletrônicos', icon: '📱', count: 245 },
  { name: 'Informática', icon: '💻', count: 189 },
  { name: 'Casa & Jardim', icon: '🏠', count: 312 },
  { name: 'Moda', icon: '👕', count: 567 },
  { name: 'Esportes', icon: '⚽', count: 198 },
  { name: 'Livros', icon: '📚', count: 423 }
];

export default function HomePage() {
  const { addItem } = useCartStore();
  const [wishlist, setWishlist] = useState<string[]>([]);

  const handleAddToCart = (product: Product) => {
    addItem({
      id: product.id,
      name: product.name,
      price: product.price,
      image: product.image,
      quantity: 1
    });
    toast.success(`${product.name} adicionado ao carrinho!`);
  };

  const toggleWishlist = (productId: string) => {
    setWishlist(prev => 
      prev.includes(productId) 
        ? prev.filter(id => id !== productId)
        : [...prev, productId]
    );
  };

  const renderStars = (rating: number) => {
    return Array.from({ length: 5 }, (_, i) => (
      <span key={i}>
        {i < Math.floor(rating) ? (
          <StarSolidIcon className="h-4 w-4 text-yellow-400" />
        ) : (
          <StarIcon className="h-4 w-4 text-gray-300" />
        )}
      </span>
    ));
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Hero Section */}
      <section className="relative bg-gradient-to-r from-primary-600 to-primary-800 text-white">
        <div className="absolute inset-0 bg-black opacity-20"></div>
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
          <div className="text-center">
            <h1 className="text-4xl md:text-6xl font-bold mb-6">
              Bem-vindo ao <span className="text-yellow-400">E-commerce Digital</span>
            </h1>
            <p className="text-xl md:text-2xl mb-8 max-w-3xl mx-auto">
              Descubra produtos incríveis com os melhores preços e entrega rápida
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link
                href="/products"
                className="bg-yellow-400 text-gray-900 px-8 py-3 rounded-lg font-semibold hover:bg-yellow-300 transition-colors"
              >
                Ver Produtos
              </Link>
              <Link
                href="/categories"
                className="border-2 border-white text-white px-8 py-3 rounded-lg font-semibold hover:bg-white hover:text-gray-900 transition-colors"
              >
                Explorar Categorias
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Categories Section */}
      <section className="py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-center mb-12">Categorias Populares</h2>
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-6">
            {categories.map((category) => (
              <Link
                key={category.name}
                href={`/categories/${category.name.toLowerCase()}`}
                className="bg-white rounded-lg p-6 text-center shadow-md hover:shadow-lg transition-shadow group"
              >
                <div className="text-4xl mb-3 group-hover:scale-110 transition-transform">
                  {category.icon}
                </div>
                <h3 className="font-semibold text-gray-900 mb-1">{category.name}</h3>
                <p className="text-sm text-gray-500">{category.count} produtos</p>
              </Link>
            ))}
          </div>
        </div>
      </section>

      {/* Featured Products */}
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold mb-4">Produtos em Destaque</h2>
            <p className="text-gray-600 max-w-2xl mx-auto">
              Confira nossa seleção especial de produtos com os melhores preços e qualidade garantida
            </p>
          </div>
          
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8">
            {featuredProducts.map((product) => (
              <div key={product.id} className="group relative bg-white rounded-lg shadow-md overflow-hidden hover:shadow-xl transition-shadow">
                <div className="relative aspect-square overflow-hidden">
                  <Image
                    src={product.image}
                    alt={product.name}
                    fill
                    className="object-cover group-hover:scale-105 transition-transform duration-300"
                  />
                  <button
                    onClick={() => toggleWishlist(product.id)}
                    className="absolute top-3 right-3 p-2 bg-white rounded-full shadow-md hover:bg-gray-50 transition-colors"
                  >
                    <HeartIcon 
                      className={`h-5 w-5 ${
                        wishlist.includes(product.id) ? 'text-red-500 fill-current' : 'text-gray-400'
                      }`} 
                    />
                  </button>
                </div>
                
                <div className="p-6">
                  <div className="flex items-center mb-2">
                    <div className="flex items-center">
                      {renderStars(product.rating)}
                    </div>
                    <span className="ml-2 text-sm text-gray-500">({product.reviews})</span>
                  </div>
                  
                  <h3 className="font-semibold text-gray-900 mb-2 line-clamp-2">
                    {product.name}
                  </h3>
                  
                  <p className="text-sm text-gray-600 mb-3 line-clamp-2">
                    {product.description}
                  </p>
                  
                  <div className="flex items-center justify-between mb-4">
                    <span className="text-2xl font-bold text-primary-600">
                      R$ {product.price.toFixed(2)}
                    </span>
                    <span className="text-sm text-gray-500">
                      {product.stock} em estoque
                    </span>
                  </div>
                  
                  <button
                    onClick={() => handleAddToCart(product)}
                    className="w-full bg-primary-600 text-white py-2 px-4 rounded-lg hover:bg-primary-700 transition-colors flex items-center justify-center gap-2"
                  >
                    <ShoppingCartIcon className="h-5 w-5" />
                    Adicionar ao Carrinho
                  </button>
                </div>
              </div>
            ))}
          </div>
          
          <div className="text-center mt-12">
            <Link
              href="/products"
              className="inline-flex items-center px-6 py-3 border border-primary-600 text-primary-600 rounded-lg hover:bg-primary-600 hover:text-white transition-colors"
            >
              Ver Todos os Produtos
            </Link>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="bg-primary-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl">🚚</span>
              </div>
              <h3 className="text-xl font-semibold mb-2">Entrega Rápida</h3>
              <p className="text-gray-600">Receba seus produtos em até 2 dias úteis</p>
            </div>
            
            <div className="text-center">
              <div className="bg-primary-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl">🔒</span>
              </div>
              <h3 className="text-xl font-semibold mb-2">Compra Segura</h3>
              <p className="text-gray-600">Seus dados protegidos com criptografia SSL</p>
            </div>
            
            <div className="text-center">
              <div className="bg-primary-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl">💳</span>
              </div>
              <h3 className="text-xl font-semibold mb-2">Pagamento Fácil</h3>
              <p className="text-gray-600">Cartão de crédito, débito e PIX</p>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}