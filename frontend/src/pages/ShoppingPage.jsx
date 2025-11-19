import React, { useState, useEffect } from 'react';
import { Search, MapPin, Clock, Star, ShoppingCart, Filter, X, Plus, Minus, Heart } from 'lucide-react';

const ShoppingPage = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [cart, setCart] = useState([]);
  const [selectedStore, setSelectedStore] = useState(null);
  const [showCart, setShowCart] = useState(false);
  const [sortBy, setSortBy] = useState('relevance');
  const [filterOpen, setFilterOpen] = useState(false);
  const [wishlist, setWishlist] = useState([]);
  const [currentLocation, setCurrentLocation] = useState('Detecting location...');
  const [showLocationModal, setShowLocationModal] = useState(false);
  const [locationError, setLocationError] = useState(null);

  // Get user's current location on component mount
  useEffect(() => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        async (position) => {
          const { latitude, longitude } = position.coords;
          try {
            // Use reverse geocoding to get address
            const response = await fetch(
              `https://nominatim.openstreetmap.org/reverse?format=json&lat=${latitude}&lon=${longitude}`
            );
            const data = await response.json();
            const address = data.address;
            const location = `${address.suburb || address.neighbourhood || address.city_district || ''}, ${address.city || address.state_district || ''}`.trim();
            setCurrentLocation(location || 'Location detected');
          } catch (error) {
            console.error('Error getting address:', error);
            setCurrentLocation('Koramangala, Bangalore');
          }
        },
        (error) => {
          console.error('Error getting location:', error);
          setLocationError('Unable to detect location');
          setCurrentLocation('Koramangala, Bangalore');
        }
      );
    } else {
      setCurrentLocation('Koramangala, Bangalore');
    }
  }, []);

  const availableLocations = [
    'Koramangala, Bangalore',
    'Indiranagar, Bangalore',
    'Whitefield, Bangalore',
    'HSR Layout, Bangalore',
    'Jayanagar, Bangalore',
    'MG Road, Bangalore',
    'Electronic City, Bangalore'
  ];

  // Sample medicine stores data
  const stores = [
    {
      id: 1,
      name: "MedPlus Pharmacy",
      rating: 4.5,
      deliveryTime: "15-20 min",
      distance: "1.2 km",
      minOrder: 0,
      deliveryFee: 20,
      image: "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?w=400&h=200&fit=crop",
      categories: ["Prescription", "OTC", "Healthcare"],
      offers: ["20% off on first order", "Free delivery above ₹500"],
      verified: true
    },
    {
      id: 2,
      name: "Apollo Pharmacy",
      rating: 4.8,
      deliveryTime: "20-25 min",
      distance: "2.1 km",
      minOrder: 100,
      deliveryFee: 30,
      image: "https://images.unsplash.com/photo-1631549916768-4119b2e5f926?w=400&h=200&fit=crop",
      categories: ["Prescription", "Baby Care", "Wellness"],
      offers: ["Flat ₹100 off on orders above ₹999"],
      verified: true
    },
    {
      id: 3,
      name: "Wellness Forever",
      rating: 4.3,
      deliveryTime: "25-30 min",
      distance: "3.5 km",
      minOrder: 150,
      deliveryFee: 40,
      image: "https://images.unsplash.com/photo-1585435557343-3b092031a831?w=400&h=200&fit=crop",
      categories: ["Vitamins", "Supplements", "Ayurvedic"],
      offers: ["Buy 2 Get 1 Free on select items"],
      verified: true
    },
    {
      id: 4,
      name: "Netmeds Local",
      rating: 4.6,
      deliveryTime: "10-15 min",
      distance: "0.8 km",
      minOrder: 0,
      deliveryFee: 15,
      image: "https://images.unsplash.com/photo-1587854692152-cbe660dbde88?w=400&h=200&fit=crop",
      categories: ["All Categories"],
      offers: ["Express delivery available"],
      verified: true
    }
  ];

  // Comprehensive list of medicines available in India
  const medicines = [
    // Pain Relief & Fever
    {
      id: 1,
      name: "Paracetamol 500mg",
      category: "Pain Relief",
      price: 25,
      mrp: 35,
      discount: 28,
      prescription: false,
      inStock: true,
      manufacturer: "GlaxoSmithKline",
      rating: 4.5,
      reviews: 234,
      image: "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=150&h=150&fit=crop",
      storeId: 1
    },
    {
      id: 2,
      name: "Dolo 650mg Tablets",
      category: "Fever & Pain",
      price: 30,
      mrp: 40,
      discount: 25,
      prescription: false,
      inStock: true,
      manufacturer: "Micro Labs",
      rating: 4.7,
      reviews: 456,
      image: "https://images.unsplash.com/photo-1471864190281-a93a3070b6de?w=150&h=150&fit=crop",
      storeId: 1
    },
    {
      id: 3,
      name: "Crocin Advance 500mg",
      category: "Pain Relief",
      price: 35,
      mrp: 45,
      discount: 22,
      prescription: false,
      inStock: true,
      manufacturer: "GSK",
      rating: 4.6,
      reviews: 321,
      image: "https://images.unsplash.com/photo-1628771065518-0d82f1938462?w=150&h=150&fit=crop",
      storeId: 3
    },
    {
      id: 4,
      name: "Ibuprofen 400mg",
      category: "Pain Relief",
      price: 40,
      mrp: 55,
      discount: 27,
      prescription: false,
      inStock: true,
      manufacturer: "Abbott",
      rating: 4.5,
      reviews: 289,
      image: "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=150&h=150&fit=crop",
      storeId: 1
    },
    {
      id: 5,
      name: "Combiflam Tablets",
      category: "Pain & Fever",
      price: 32,
      mrp: 42,
      discount: 24,
      prescription: false,
      inStock: true,
      manufacturer: "Sanofi",
      rating: 4.6,
      reviews: 412,
      image: "https://images.unsplash.com/photo-1471864190281-a93a3070b6de?w=150&h=150&fit=crop",
      storeId: 2
    },
    // Cough & Cold
    {
      id: 6,
      name: "Benadryl Cough Syrup 100ml",
      category: "Cough & Cold",
      price: 95,
      mrp: 115,
      discount: 17,
      prescription: false,
      inStock: true,
      manufacturer: "Johnson & Johnson",
      rating: 4.4,
      reviews: 267,
      image: "https://images.unsplash.com/photo-1587854692152-cbe660dbde88?w=150&h=150&fit=crop",
      storeId: 1
    },
    {
      id: 7,
      name: "Chericof Syrup 100ml",
      category: "Cough & Cold",
      price: 85,
      mrp: 100,
      discount: 15,
      prescription: false,
      inStock: true,
      manufacturer: "Mankind",
      rating: 4.3,
      reviews: 178,
      image: "https://images.unsplash.com/photo-1587854692152-cbe660dbde88?w=150&h=150&fit=crop",
      storeId: 2
    },
    {
      id: 8,
      name: "Vicks Action 500",
      category: "Cold & Flu",
      price: 45,
      mrp: 58,
      discount: 22,
      prescription: false,
      inStock: true,
      manufacturer: "P&G",
      rating: 4.5,
      reviews: 345,
      image: "https://images.unsplash.com/photo-1628771065518-0d82f1938462?w=150&h=150&fit=crop",
      storeId: 1
    },
    // Allergy
    {
      id: 9,
      name: "Cetirizine 10mg",
      category: "Allergy",
      price: 15,
      mrp: 20,
      discount: 25,
      prescription: false,
      inStock: true,
      manufacturer: "Cipla",
      rating: 4.3,
      reviews: 145,
      image: "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=150&h=150&fit=crop",
      storeId: 1
    },
    {
      id: 10,
      name: "Allegra 120mg",
      category: "Allergy",
      price: 125,
      mrp: 150,
      discount: 17,
      prescription: false,
      inStock: true,
      manufacturer: "Sanofi",
      rating: 4.6,
      reviews: 234,
      image: "https://images.unsplash.com/photo-1471864190281-a93a3070b6de?w=150&h=150&fit=crop",
      storeId: 2
    },
    // Vitamins & Supplements
    {
      id: 11,
      name: "Vitamin D3 60K",
      category: "Vitamins",
      price: 45,
      mrp: 60,
      discount: 25,
      prescription: true,
      inStock: true,
      manufacturer: "Sun Pharma",
      rating: 4.4,
      reviews: 189,
      image: "https://images.unsplash.com/photo-1550572017-edd951aa8f72?w=150&h=150&fit=crop",
      storeId: 2
    },
    {
      id: 12,
      name: "Omega 3 Capsules",
      category: "Supplements",
      price: 350,
      mrp: 450,
      discount: 22,
      prescription: false,
      inStock: true,
      manufacturer: "HealthVit",
      rating: 4.5,
      reviews: 267,
      image: "https://images.unsplash.com/photo-1526161140091-32b9e0b9f320?w=150&h=150&fit=crop",
      storeId: 3
    },
    {
      id: 13,
      name: "Vitamin C 500mg",
      category: "Vitamins",
      price: 180,
      mrp: 220,
      discount: 18,
      prescription: false,
      inStock: true,
      manufacturer: "HealthKart",
      rating: 4.4,
      reviews: 312,
      image: "https://images.unsplash.com/photo-1550572017-edd951aa8f72?w=150&h=150&fit=crop",
      storeId: 3
    },
    {
      id: 14,
      name: "Multivitamin Tablets",
      category: "Vitamins",
      price: 250,
      mrp: 320,
      discount: 22,
      prescription: false,
      inStock: true,
      manufacturer: "Himalaya",
      rating: 4.5,
      reviews: 428,
      image: "https://images.unsplash.com/photo-1526161140091-32b9e0b9f320?w=150&h=150&fit=crop",
      storeId: 2
    },
    {
      id: 15,
      name: "Calcium + Vitamin D3",
      category: "Supplements",
      price: 195,
      mrp: 240,
      discount: 19,
      prescription: false,
      inStock: true,
      manufacturer: "Cipla",
      rating: 4.3,
      reviews: 189,
      image: "https://images.unsplash.com/photo-1550572017-edd951aa8f72?w=150&h=150&fit=crop",
      storeId: 1
    },
    // Antibiotics
    {
      id: 16,
      name: "Azithromycin 500mg",
      category: "Antibiotics",
      price: 85,
      mrp: 110,
      discount: 23,
      prescription: true,
      inStock: true,
      manufacturer: "Cipla",
      rating: 4.6,
      reviews: 167,
      image: "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=150&h=150&fit=crop",
      storeId: 1
    },
    {
      id: 17,
      name: "Amoxicillin 500mg",
      category: "Antibiotics",
      price: 45,
      mrp: 60,
      discount: 25,
      prescription: true,
      inStock: true,
      manufacturer: "Ranbaxy",
      rating: 4.5,
      reviews: 145,
      image: "https://images.unsplash.com/photo-1471864190281-a93a3070b6de?w=150&h=150&fit=crop",
      storeId: 2
    },
    // Digestive Health
    {
      id: 18,
      name: "Pan 40 Tablets",
      category: "Digestive",
      price: 120,
      mrp: 155,
      discount: 23,
      prescription: true,
      inStock: true,
      manufacturer: "Alkem",
      rating: 4.6,
      reviews: 298,
      image: "https://images.unsplash.com/photo-1628771065518-0d82f1938462?w=150&h=150&fit=crop",
      storeId: 1
    },
    {
      id: 19,
      name: "Digene Tablets",
      category: "Antacid",
      price: 28,
      mrp: 35,
      discount: 20,
      prescription: false,
      inStock: true,
      manufacturer: "Abbott",
      rating: 4.4,
      reviews: 412,
      image: "https://images.unsplash.com/photo-1471864190281-a93a3070b6de?w=150&h=150&fit=crop",
      storeId: 1
    },
    {
      id: 20,
      name: "Isabgol Husk 100g",
      category: "Digestive",
      price: 95,
      mrp: 115,
      discount: 17,
      prescription: false,
      inStock: true,
      manufacturer: "Dabur",
      rating: 4.5,
      reviews: 234,
      image: "https://images.unsplash.com/photo-1550572017-edd951aa8f72?w=150&h=150&fit=crop",
      storeId: 3
    },
    // Diabetes
    {
      id: 21,
      name: "Metformin 500mg",
      category: "Diabetes",
      price: 45,
      mrp: 65,
      discount: 31,
      prescription: true,
      inStock: true,
      manufacturer: "Sun Pharma",
      rating: 4.5,
      reviews: 189,
      image: "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=150&h=150&fit=crop",
      storeId: 2
    },
    {
      id: 22,
      name: "Glimepiride 2mg",
      category: "Diabetes",
      price: 85,
      mrp: 110,
      discount: 23,
      prescription: true,
      inStock: true,
      manufacturer: "Torrent",
      rating: 4.4,
      reviews: 156,
      image: "https://images.unsplash.com/photo-1471864190281-a93a3070b6de?w=150&h=150&fit=crop",
      storeId: 1
    },
    // Blood Pressure
    {
      id: 23,
      name: "Amlodipine 5mg",
      category: "Blood Pressure",
      price: 35,
      mrp: 50,
      discount: 30,
      prescription: true,
      inStock: true,
      manufacturer: "Cipla",
      rating: 4.6,
      reviews: 267,
      image: "https://images.unsplash.com/photo-1628771065518-0d82f1938462?w=150&h=150&fit=crop",
      storeId: 1
    },
    {
      id: 24,
      name: "Telmisartan 40mg",
      category: "Blood Pressure",
      price: 95,
      mrp: 125,
      discount: 24,
      prescription: true,
      inStock: true,
      manufacturer: "Glenmark",
      rating: 4.5,
      reviews: 198,
      image: "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=150&h=150&fit=crop",
      storeId: 2
    },
    // First Aid
    {
      id: 25,
      name: "Dettol Antiseptic Liquid 500ml",
      category: "First Aid",
      price: 165,
      mrp: 195,
      discount: 15,
      prescription: false,
      inStock: true,
      manufacturer: "Reckitt",
      rating: 4.7,
      reviews: 523,
      image: "https://images.unsplash.com/photo-1587854692152-cbe660dbde88?w=150&h=150&fit=crop",
      storeId: 1
    },
    {
      id: 26,
      name: "Betadine Solution 100ml",
      category: "First Aid",
      price: 145,
      mrp: 170,
      discount: 15,
      prescription: false,
      inStock: true,
      manufacturer: "Win Medicare",
      rating: 4.6,
      reviews: 312,
      image: "https://images.unsplash.com/photo-1587854692152-cbe660dbde88?w=150&h=150&fit=crop",
      storeId: 2
    },
    {
      id: 27,
      name: "Band-Aid Strips (100 pcs)",
      category: "First Aid",
      price: 95,
      mrp: 120,
      discount: 21,
      prescription: false,
      inStock: true,
      manufacturer: "Johnson & Johnson",
      rating: 4.5,
      reviews: 445,
      image: "https://images.unsplash.com/photo-1628771065518-0d82f1938462?w=150&h=150&fit=crop",
      storeId: 1
    },
    // Baby Care
    {
      id: 28,
      name: "Calpol 250mg Syrup",
      category: "Baby Care",
      price: 65,
      mrp: 80,
      discount: 19,
      prescription: false,
      inStock: true,
      manufacturer: "GSK",
      rating: 4.7,
      reviews: 389,
      image: "https://images.unsplash.com/photo-1587854692152-cbe660dbde88?w=150&h=150&fit=crop",
      storeId: 1
    },
    {
      id: 29,
      name: "Gripe Water 100ml",
      category: "Baby Care",
      price: 55,
      mrp: 70,
      discount: 21,
      prescription: false,
      inStock: true,
      manufacturer: "Woodwards",
      rating: 4.6,
      reviews: 267,
      image: "https://images.unsplash.com/photo-1587854692152-cbe660dbde88?w=150&h=150&fit=crop",
      storeId: 2
    },
    {
      id: 30,
      name: "Baby Powder 200g",
      category: "Baby Care",
      price: 125,
      mrp: 145,
      discount: 14,
      prescription: false,
      inStock: true,
      manufacturer: "Johnson's",
      rating: 4.7,
      reviews: 512,
      image: "https://images.unsplash.com/photo-1550572017-edd951aa8f72?w=150&h=150&fit=crop",
      storeId: 3
    }
  ];

  const categories = [
    { id: 'all', name: 'All', icon: '🏥' },
    { id: 'prescription', name: 'Prescription', icon: '📋' },
    { id: 'otc', name: 'OTC Medicines', icon: '💊' },
    { id: 'vitamins', name: 'Vitamins', icon: '🌿' },
    { id: 'babycare', name: 'Baby Care', icon: '👶' },
    { id: 'personalcare', name: 'Personal Care', icon: '🧴' },
    { id: 'healthcare', name: 'Healthcare Devices', icon: '🩺' },
    { id: 'ayurvedic', name: 'Ayurvedic', icon: '🍃' }
  ];

  const addToCart = (medicine) => {
    const existingItem = cart.find(item => item.id === medicine.id);
    if (existingItem) {
      setCart(cart.map(item =>
        item.id === medicine.id
          ? { ...item, quantity: item.quantity + 1 }
          : item
      ));
    } else {
      setCart([...cart, { ...medicine, quantity: 1 }]);
    }
  };

  const removeFromCart = (medicineId) => {
    const existingItem = cart.find(item => item.id === medicineId);
    if (existingItem.quantity > 1) {
      setCart(cart.map(item =>
        item.id === medicineId
          ? { ...item, quantity: item.quantity - 1 }
          : item
      ));
    } else {
      setCart(cart.filter(item => item.id !== medicineId));
    }
  };

  const toggleWishlist = (medicineId) => {
    if (wishlist.includes(medicineId)) {
      setWishlist(wishlist.filter(id => id !== medicineId));
    } else {
      setWishlist([...wishlist, medicineId]);
    }
  };

  const cartTotal = cart.reduce((total, item) => total + (item.price * item.quantity), 0);
  const cartItemCount = cart.reduce((total, item) => total + item.quantity, 0);

  const filteredMedicines = medicines.filter(med => {
    const searchLower = searchQuery.toLowerCase();
    return (
      med.name.toLowerCase().includes(searchLower) ||
      med.category.toLowerCase().includes(searchLower) ||
      med.manufacturer.toLowerCase().includes(searchLower)
    );
  });

  // Sort filtered medicines
  const sortedMedicines = [...filteredMedicines].sort((a, b) => {
    switch (sortBy) {
      case 'price-low':
        return a.price - b.price;
      case 'price-high':
        return b.price - a.price;
      case 'rating':
        return b.rating - a.rating;
      case 'discount':
        return b.discount - a.discount;
      default:
        return 0; // relevance
    }
  });

  return (
    <div className="h-full bg-gray-50 overflow-y-auto">
      {/* Header */}
      <div className="bg-white shadow-sm sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-4 py-4">
          {/* Location */}
          <button
            onClick={() => setShowLocationModal(true)}
            className="flex items-center gap-2 mb-3 hover:bg-gray-50 p-2 rounded-lg transition -ml-2"
          >
            <MapPin className="w-5 h-5 text-blue-600" />
            <div className="text-left">
              <div className="font-semibold text-sm flex items-center gap-1">
                Delivering to
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                </svg>
              </div>
              <div className="text-xs text-gray-600">{currentLocation}</div>
            </div>
          </button>

          {/* Search Bar */}
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
            <input
              type="text"
              placeholder="Search for medicines, health products..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-12 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
        </div>
      </div>

      {/* Categories Scroll */}
      <div className="bg-white border-b overflow-x-auto sticky top-[120px] z-30">
        <div className="max-w-7xl mx-auto px-4 py-3">
          <div className="flex gap-4 min-w-max">
            {categories.map(cat => (
              <button
                key={cat.id}
                onClick={() => setSelectedCategory(cat.id)}
                className={`flex flex-col items-center gap-1 px-3 py-2 rounded-lg transition ${
                  selectedCategory === cat.id
                    ? 'bg-blue-50 text-blue-600'
                    : 'text-gray-600 hover:bg-gray-50'
                }`}
              >
                <span className="text-2xl">{cat.icon}</span>
                <span className="text-xs whitespace-nowrap">{cat.name}</span>
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 py-6">
        {/* Filters and Sort */}
        <div className="flex justify-between items-center mb-6">
          <div className="text-sm text-gray-600">
            {sortedMedicines.length} medicine{sortedMedicines.length !== 1 ? 's' : ''} available
            {searchQuery && ` for "${searchQuery}"`}
          </div>
          <div className="flex gap-2">
            <button
              onClick={() => setFilterOpen(!filterOpen)}
              className="px-4 py-2 border border-gray-300 rounded-lg flex items-center gap-2 hover:bg-gray-50"
            >
              <Filter className="w-4 h-4" />
              Filters
            </button>
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
              className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
            >
              <option value="relevance">Relevance</option>
              <option value="price-low">Price: Low to High</option>
              <option value="price-high">Price: High to Low</option>
              <option value="rating">Rating</option>
              <option value="discount">Discount</option>
            </select>
          </div>
        </div>

        {/* Store Listings */}
        <div className="mb-8">
          <h2 className="text-xl font-bold mb-4">Medicine Stores Near You</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {stores.map(store => (
              <div
                key={store.id}
                onClick={() => setSelectedStore(store)}
                className="bg-white rounded-xl shadow-sm hover:shadow-md transition cursor-pointer overflow-hidden"
              >
                <div className="relative">
                  <img
                    src={store.image}
                    alt={store.name}
                    className="w-full h-40 object-cover"
                  />
                  {store.verified && (
                    <div className="absolute top-2 right-2 bg-green-500 text-white px-2 py-1 rounded-full text-xs font-semibold">
                      Verified
                    </div>
                  )}
                </div>
                <div className="p-4">
                  <h3 className="font-bold text-lg mb-2">{store.name}</h3>
                  <div className="flex items-center gap-4 text-sm text-gray-600 mb-3">
                    <div className="flex items-center gap-1">
                      <Star className="w-4 h-4 fill-yellow-400 text-yellow-400" />
                      <span>{store.rating}</span>
                    </div>
                    <div className="flex items-center gap-1">
                      <Clock className="w-4 h-4" />
                      <span>{store.deliveryTime}</span>
                    </div>
                    <div className="flex items-center gap-1">
                      <MapPin className="w-4 h-4" />
                      <span>{store.distance}</span>
                    </div>
                  </div>
                  <div className="flex flex-wrap gap-2 mb-3">
                    {store.categories.map((cat, idx) => (
                      <span key={idx} className="text-xs bg-gray-100 px-2 py-1 rounded">
                        {cat}
                      </span>
                    ))}
                  </div>
                  {store.offers.length > 0 && (
                    <div className="bg-blue-50 text-blue-700 text-xs px-3 py-2 rounded">
                      🎉 {store.offers[0]}
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Medicine Products Grid */}
        <div>
          <h2 className="text-xl font-bold mb-4">
            {searchQuery ? `Search Results for "${searchQuery}"` : 'Popular Medicines'}
          </h2>
          {sortedMedicines.length === 0 ? (
            <div className="text-center py-16">
              <div className="text-gray-400 mb-4">
                <Search className="w-16 h-16 mx-auto mb-4" />
                <p className="text-xl font-semibold">No medicines found</p>
                <p className="text-sm mt-2">Try searching with different keywords</p>
              </div>
            </div>
          ) : (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
              {sortedMedicines.map(medicine => (
              <div
                key={medicine.id}
                className="bg-white rounded-xl shadow-sm hover:shadow-md transition overflow-hidden"
              >
                <div className="relative">
                  <img
                    src={medicine.image}
                    alt={medicine.name}
                    className="w-full h-40 object-cover"
                  />
                  <button
                    onClick={() => toggleWishlist(medicine.id)}
                    className="absolute top-2 right-2 bg-white p-2 rounded-full shadow-md hover:scale-110 transition"
                  >
                    <Heart
                      className={`w-5 h-5 ${
                        wishlist.includes(medicine.id)
                          ? 'fill-red-500 text-red-500'
                          : 'text-gray-400'
                      }`}
                    />
                  </button>
                  {medicine.discount > 0 && (
                    <div className="absolute top-2 left-2 bg-green-500 text-white px-2 py-1 rounded text-xs font-bold">
                      {medicine.discount}% OFF
                    </div>
                  )}
                  {medicine.prescription && (
                    <div className="absolute bottom-2 left-2 bg-red-500 text-white px-2 py-1 rounded text-xs">
                      Rx Required
                    </div>
                  )}
                </div>
                <div className="p-4">
                  <div className="text-xs text-gray-500 mb-1">{medicine.category}</div>
                  <h3 className="font-semibold text-sm mb-1 line-clamp-2">{medicine.name}</h3>
                  <div className="text-xs text-gray-500 mb-2">{medicine.manufacturer}</div>
                  
                  <div className="flex items-center gap-1 mb-2">
                    <Star className="w-3 h-3 fill-yellow-400 text-yellow-400" />
                    <span className="text-xs text-gray-600">
                      {medicine.rating} ({medicine.reviews})
                    </span>
                  </div>

                  <div className="flex items-baseline gap-2 mb-3">
                    <span className="font-bold text-lg">₹{medicine.price}</span>
                    <span className="text-xs text-gray-400 line-through">₹{medicine.mrp}</span>
                  </div>

                  {medicine.inStock ? (
                    <button
                      onClick={() => addToCart(medicine)}
                      className="w-full bg-blue-600 hover:bg-blue-700 text-white py-2 rounded-lg text-sm font-semibold transition flex items-center justify-center gap-2"
                    >
                      <Plus className="w-4 h-4" />
                      Add to Cart
                    </button>
                  ) : (
                    <button
                      disabled
                      className="w-full bg-gray-200 text-gray-500 py-2 rounded-lg text-sm font-semibold cursor-not-allowed"
                    >
                      Out of Stock
                    </button>
                  )}
                </div>
              </div>
            ))}
            </div>
          )}
        </div>
      </div>

      {/* Cart Button */}
      {cart.length > 0 && (
        <button
          onClick={() => setShowCart(true)}
          className="fixed bottom-6 right-6 bg-blue-600 hover:bg-blue-700 text-white px-6 py-4 rounded-full shadow-2xl flex items-center gap-3 transition z-50"
        >
          <ShoppingCart className="w-6 h-6" />
          <div className="text-left">
            <div className="text-xs opacity-90">{cartItemCount} items</div>
            <div className="font-bold">₹{cartTotal}</div>
          </div>
        </button>
      )}

      {/* Cart Sidebar */}
      {showCart && (
        <div className="fixed inset-0 bg-black bg-opacity-50 z-50">
          <div className="absolute right-0 top-0 h-full w-full max-w-md bg-white shadow-xl overflow-y-auto">
            <div className="sticky top-0 bg-white border-b p-4 flex justify-between items-center">
              <h2 className="text-xl font-bold">Your Cart ({cartItemCount})</h2>
              <button
                onClick={() => setShowCart(false)}
                className="p-2 hover:bg-gray-100 rounded-full"
              >
                <X className="w-6 h-6" />
              </button>
            </div>

            <div className="p-4 space-y-4">
              {cart.map(item => (
                <div key={item.id} className="flex gap-4 bg-gray-50 p-3 rounded-lg">
                  <img
                    src={item.image}
                    alt={item.name}
                    className="w-20 h-20 object-cover rounded"
                  />
                  <div className="flex-1">
                    <h4 className="font-semibold text-sm mb-1">{item.name}</h4>
                    <div className="text-sm text-gray-600 mb-2">₹{item.price}</div>
                    <div className="flex items-center gap-2">
                      <button
                        onClick={() => removeFromCart(item.id)}
                        className="p-1 bg-white border rounded hover:bg-gray-100"
                      >
                        <Minus className="w-4 h-4" />
                      </button>
                      <span className="font-semibold">{item.quantity}</span>
                      <button
                        onClick={() => addToCart(item)}
                        className="p-1 bg-white border rounded hover:bg-gray-100"
                      >
                        <Plus className="w-4 h-4" />
                      </button>
                    </div>
                  </div>
                  <div className="font-bold">₹{item.price * item.quantity}</div>
                </div>
              ))}
            </div>

            <div className="sticky bottom-0 bg-white border-t p-4 space-y-3">
              <div className="flex justify-between text-sm">
                <span>Subtotal</span>
                <span>₹{cartTotal}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span>Delivery Fee</span>
                <span>₹30</span>
              </div>
              <div className="flex justify-between font-bold text-lg border-t pt-2">
                <span>Total</span>
                <span>₹{cartTotal + 30}</span>
              </div>
              <button className="w-full bg-green-600 hover:bg-green-700 text-white py-3 rounded-lg font-bold transition">
                Proceed to Checkout
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Location Selection Modal */}
      {showLocationModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-xl shadow-2xl max-w-md w-full max-h-[80vh] overflow-hidden">
            <div className="sticky top-0 bg-white border-b p-4 flex justify-between items-center">
              <h2 className="text-xl font-bold">Select Location</h2>
              <button
                onClick={() => setShowLocationModal(false)}
                className="p-2 hover:bg-gray-100 rounded-full"
              >
                <X className="w-6 h-6" />
              </button>
            </div>
            
            <div className="p-4 space-y-2 overflow-y-auto max-h-[60vh]">
              {availableLocations.map((location, index) => (
                <button
                  key={index}
                  onClick={() => {
                    setCurrentLocation(location);
                    setShowLocationModal(false);
                  }}
                  className={`w-full text-left p-4 rounded-lg border-2 transition ${
                    currentLocation === location
                      ? 'border-blue-600 bg-blue-50'
                      : 'border-gray-200 hover:border-blue-300 hover:bg-gray-50'
                  }`}
                >
                  <div className="flex items-center gap-3">
                    <MapPin className={`w-5 h-5 ${
                      currentLocation === location ? 'text-blue-600' : 'text-gray-400'
                    }`} />
                    <div className="flex-1">
                      <div className="font-semibold">{location}</div>
                      <div className="text-xs text-gray-500">Available for delivery</div>
                    </div>
                    {currentLocation === location && (
                      <div className="w-6 h-6 bg-blue-600 rounded-full flex items-center justify-center">
                        <svg className="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 20 20">
                          <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                        </svg>
                      </div>
                    )}
                  </div>
                </button>
              ))}
            </div>
            
            <div className="sticky bottom-0 bg-white border-t p-4">
              <button
                onClick={() => setShowLocationModal(false)}
                className="w-full bg-blue-600 hover:bg-blue-700 text-white py-3 rounded-lg font-bold transition"
              >
                Confirm Location
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ShoppingPage;
