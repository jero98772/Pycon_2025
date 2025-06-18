use pyo3::prelude::*;
#[pyfunction]
fn add_numbers(a: i32, b: i32) -> i32 {
    a + b
}
#[pymodule]
fn pyo3_example(py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(add_numbers, m)?)?;
    Ok(())
}
