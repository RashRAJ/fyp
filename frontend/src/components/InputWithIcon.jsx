function InputWithIcon(props) {
  return (
    <form className="flex flex-col w-full mx-auto mb-2">
      <label className="text-primary-300 text-sm font-medium pb-1">{props.label}</label>
      <div className="relative w-full">
        <div className="absolute inset-y-0 start-0 flex items-center ps-3 pointer-events-none">{props.leftIcon}</div>
        <input
          type="text"
          id="voice-search"
          className="border bg-transparent py-4 border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full ps-10 p-2.5  "
          {...props}
          required
        />
        <button type="button" className="absolute inset-y-0 end-0 flex items-center pe-3" onClick={props.handleRightIconClick}>
          {props.rightIcon}
        </button>
      </div>
    </form>
  );
}

export default InputWithIcon;
