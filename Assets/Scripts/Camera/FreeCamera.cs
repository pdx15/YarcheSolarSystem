using UnityEngine;

public class FreeCamera : MonoBehaviour
{
    public float speed = 50f;
    public float sensitivity = 2f;

    float rotX;
    float rotY;

    void Update()
    {
        float x = Input.GetAxis("Horizontal");
        float z = Input.GetAxis("Vertical");

        transform.position += transform.forward * z * speed * Time.deltaTime;
        transform.position += transform.right * x * speed * Time.deltaTime;

        if (Input.GetMouseButton(1))
        {
            rotX += Input.GetAxis("Mouse X") * sensitivity;
            rotY -= Input.GetAxis("Mouse Y") * sensitivity;

            rotY = Mathf.Clamp(rotY, -90, 90);

            transform.rotation = Quaternion.Euler(rotY, rotX, 0);
        }
    }
}