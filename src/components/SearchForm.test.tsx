import { describe, it, expect, vi } from "vitest"
import { render, screen, fireEvent } from "@testing-library/react"
import { SearchForm } from "./SearchForm"

describe("SearchForm", () => {
  const defaultProps = {
    defaultKeyword: "restaurants",
    defaultLocation: "Chicago",
    defaultRadius: 50,
    defaultMaxResults: 60,
    onSearch: vi.fn(),
    isPending: false,
  }

  it("renders with default values", () => {
    render(<SearchForm {...defaultProps} />)

    expect(screen.getByLabelText("Keyword")).toHaveValue("restaurants")
    expect(screen.getByLabelText("Location")).toHaveValue("Chicago")
    expect(screen.getByLabelText("Radius (km)")).toHaveValue(50)
    expect(screen.getByLabelText("Max Results")).toHaveValue(60)
  })

  it("calls onSearch with form values on submit", () => {
    const onSearch = vi.fn()
    render(<SearchForm {...defaultProps} onSearch={onSearch} />)

    fireEvent.click(screen.getByRole("button", { name: /search/i }))

    expect(onSearch).toHaveBeenCalledWith({
      keyword: "restaurants",
      location: "Chicago",
      radius: 50,
      max_results: 60,
    })
  })

  it("disables button when keyword is empty", () => {
    render(<SearchForm {...defaultProps} defaultKeyword="" />)
    expect(screen.getByRole("button", { name: /search/i })).toBeDisabled()
  })

  it("disables button when location is empty", () => {
    render(<SearchForm {...defaultProps} defaultLocation="" />)
    expect(screen.getByRole("button", { name: /search/i })).toBeDisabled()
  })

  it("shows loading state when pending", () => {
    render(<SearchForm {...defaultProps} isPending />)
    expect(screen.getByRole("button", { name: /searching/i })).toBeDisabled()
  })

  it("updates values on input change", () => {
    const onSearch = vi.fn()
    render(<SearchForm {...defaultProps} onSearch={onSearch} />)

    fireEvent.change(screen.getByLabelText("Keyword"), {
      target: { value: "cafes" },
    })
    fireEvent.click(screen.getByRole("button", { name: /search/i }))

    expect(onSearch).toHaveBeenCalledWith(
      expect.objectContaining({ keyword: "cafes" }),
    )
  })
})
