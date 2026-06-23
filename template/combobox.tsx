
/**
 * MultiSelectCombobox Component
 * @param {Array} options - List of objects: [{ id: '1', label: 'Option A' }]
 * @param {Array} value - Selected ids array: ['1', '2']
 * @param {Function} onChange - Callback triggered on change: (newSelectedIds) => {}
 * @param {string} label - Label shown above the combobox
 * @param {string} placeholder - Default text when nothing is selected
 * @param {string} searchPlaceholder - Placeholder inside the search field
 */
export function MultiSelectCombobox({
  options = [],
  value = [],
  onChange,
  label = "Loại hình",
  placeholder = "Chọn loại hình",
  searchPlaceholder = "Tìm kiếm"
}) {
  const [isOpen, setIsOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const popoverRef = useRef(null);

  // Auto dismiss popover when clicking outside
  useEffect(() => {
    function handleClickOutside(event) {
      if (popoverRef.current && !popoverRef.current.contains(event.target)) {
        setIsOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);

  // Filter list by search query input
  const filteredOptions = useMemo(() => {
    if (!searchQuery.trim()) return options;
    return options.filter(option =>
      option.label.toLowerCase().includes(searchQuery.toLowerCase())
    );
  }, [options, searchQuery]);

  // Toggle selection state for a single option
  const handleToggleOption = (id) => {
    const updatedValues = value.includes(id)
      ? value.filter(item => item !== id)
      : [...value, id];
    onChange(updatedValues);
  };

  // Remove tag chip directly from input field (prevents closing popover)
  const handleRemoveOption = (e, id) => {
    e.stopPropagation();
    onChange(value.filter(item => item !== id));
  };

  // Check if all currently filtered options are selected
  const isAllSelected = useMemo(() => {
    if (filteredOptions.length === 0) return false;
    return filteredOptions.every(opt => value.includes(opt.id));
  }, [filteredOptions, value]);

  // Toggle select/deselect all currently filtered items
  const handleToggleSelectAll = () => {
    if (isAllSelected) {
      const filteredIds = filteredOptions.map(opt => opt.id);
      onChange(value.filter(id => !filteredIds.includes(id)));
    } else {
      const newSelections = new Set([...value, ...filteredOptions.map(opt => opt.id)]);
      onChange(Array.from(newSelections));
    }
  };

  return (
    <div className="relative w-full" ref={popoverRef}>
      
      {/* Field Label */}
      {label && (
        <label className="block text-[15px] font-semibold text-gray-900 mb-2 select-none">
          {label}
        </label>
      )}

      {/* Input Box Trigger */}
      <div
        onClick={() => setIsOpen(!isOpen)}
        className={`w-full flex items-center justify-between min-h-[46px] px-3 py-1.5 bg-white border ${
          isOpen ? 'border-[#FF9F00] ring-2 ring-amber-100' : 'border-gray-200'
        } rounded-[20px] transition-all cursor-pointer focus:outline-none`}
      >
        {/* Chips Container */}
        <div className="flex flex-wrap gap-1.5 items-center flex-1 pr-2">
          {value.length === 0 ? (
            <span className="text-gray-400 text-[15px] pl-1.5 select-none">
              {placeholder}
            </span>
          ) : (
            value.map(id => {
              const option = options.find(o => o.id === id);
              if (!option) return null;
              return (
                <span 
                  key={id} 
                  className="inline-flex items-center gap-1 pl-2.5 pr-1.5 py-0.5 bg-gray-100 hover:bg-gray-200 text-gray-800 text-[13px] font-medium rounded-full transition-colors group select-none animate-in fade-in zoom-in-95 duration-100"
                >
                  {option.label}
                  <button
                    type="button"
                    onClick={(e) => handleRemoveOption(e, id)}
                    className="p-0.5 rounded-full hover:bg-gray-300 text-gray-500 group-hover:text-gray-800 transition-colors"
                  >
                    <SmallCloseIcon />
                  </button>
                </span>
              );
            })
          )}
        </div>

        <ChevronDownIcon />
      </div>

      {/* Popover Menu Dropdown */}
      {isOpen && (
        <div className="absolute left-0 mt-1.5 w-full bg-white border border-gray-100 shadow-xl rounded-2xl overflow-hidden z-50 animate-in fade-in slide-in-from-top-2 duration-150">
          
          {/* Popover Header: Select All & Search */}
          <div className="flex items-center px-4 py-3 border-b border-gray-100 gap-3">
            
            {/* Checkbox for Select All */}
            <button
              type="button"
              onClick={handleToggleSelectAll}
              className={`w-6 h-6 rounded-md flex items-center justify-center border transition-all shrink-0 ${
                isAllSelected
                  ? 'bg-[#FF9F00] border-[#FF9F00] shadow-sm'
                  : 'border-gray-300 hover:border-amber-500 bg-white'
              }`}
            >
              {isAllSelected && <CheckIcon />}
            </button>

            {/* Interactive Search Bar */}
            <div className="flex-1 flex items-center bg-white border border-gray-200 rounded-xl px-3 py-2 focus-within:border-[#FF9F00] transition-colors">
              <span className="mr-2 shrink-0">
                <SearchIcon />
              </span>
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder={searchPlaceholder}
                className="w-full text-[15px] text-gray-800 placeholder-gray-400 focus:outline-none bg-transparent"
              />
              {searchQuery && (
                <button 
                  onClick={() => setSearchQuery('')}
                  className="ml-1 p-0.5 rounded-full hover:bg-gray-100 shrink-0"
                >
                  <XIcon />
                </button>
              )}
            </div>
          </div>

          {/* List of Options */}
          <div className="max-h-[260px] overflow-y-auto py-1.5">
            {filteredOptions.length > 0 ? (
              filteredOptions.map((option) => {
                const isChecked = value.includes(option.id);
                return (
                  <div
                    key={option.id}
                    onClick={() => handleToggleOption(option.id)}
                    className={`flex items-center px-4 py-3 gap-3 cursor-pointer transition-colors ${
                      isChecked 
                        ? 'bg-blue-50 text-blue-600 font-medium'
                        : 'text-gray-800 hover:bg-gray-50'
                    }`}
                  >
                    {/* Orange Checkbox */}
                    <div
                      className={`w-6 h-6 rounded-md flex items-center justify-center border transition-all shrink-0 ${
                        isChecked
                          ? 'bg-[#FF9F00] border-[#FF9F00] shadow-sm'
                          : 'border-gray-300 hover:border-[#FF9F00] bg-white'
                      }`}
                    >
                      {isChecked && <CheckIcon />}
                    </div>

                    {/* Option Text */}
                    <span className={`text-[15px] select-none ${isChecked ? 'text-blue-600' : 'text-gray-700'}`}>
                      {option.label}
                    </span>
                  </div>
                );
              })
            ) : (
              <div className="py-8 text-center text-sm text-gray-400 select-none">
                Không tìm thấy kết quả phù hợp
              </div>
            )}
          </div>

        </div>
      )}

    </div>
  );
}
