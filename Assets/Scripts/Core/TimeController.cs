using UnityEngine;

public class TimeController : MonoBehaviour
{
    public double timeScale = 500;
    public double et = 0;

    void Start()
    {
        et = 2451545.0;
    }

    void Update()
    {
        et += Time.deltaTime * timeScale;
    }

    public void SetScale(double scale)
    {
        timeScale = scale;
    }
}